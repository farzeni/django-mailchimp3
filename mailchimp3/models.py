from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .client import Mailchimp

ENDPOINTS = {
    'List': {
        'resource': 'lists',
        'endpoint': 'lists'
    },

    'Member': {
        'resource': 'member',
        'endpoint': 'lists/%s/members'
    }
}


class BaseChimpManager(models.Manager):
    def __init__(self):
        super(BaseChimpManager, self).__init__()
        self.mailchimp = Mailchimp()

class BaseChimpModel(models.Model):
    def __init__(self, *args, **kwargs):
        super(BaseChimpModel, self).__init__(*args, **kwargs)
        self.mailchimp = Mailchimp()

    def get_resource(self):
        return ENDPOINTS[self.__class__.__name__]['resource']

    def get_endpoint(self):
        return ENDPOINTS[self.__class__.__name__]['endpoint']

    def request(self, args={}, method='GET'):
        return self.mailchimp.request(self.get_resource(), self.get_endpoint(), method, args)
                                        



class ListManager(BaseChimpManager):
    endpoint = ENDPOINTS['List']['endpoint']
    resource = ENDPOINTS['List']['resource']

    def get_by_name(self, list_id):
        return List.objects.filter(name=list_id).first()

    def load(self):
        lists = self.mailchimp.request(self.resource, self.endpoint)
        for m_list in lists:
            print "Found %s -> %s" % (m_list['name'], m_list['id'])
            l, created = List.objects.get_or_create(name=m_list['name'], mailchimp_id=m_list['id']) 
            print l.name , ": " , created


class List(BaseChimpModel):
    name = models.CharField(max_length=100)
    mailchimp_id = models.CharField(max_length=20)
    
    objects = ListManager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'mailchimp3'



class MemberManager(BaseChimpManager):
    endpoint = ENDPOINTS['Member']['endpoint']
    resource = ENDPOINTS['Member']['resource']

    def load(self, list_id):
        mailchimp = Mailchimp()
        
        m_list = List.objects.filter(mailchimp_id=list_id).first()
        response = self.mailchimp.request(self.resource, self.endpoint % list_id)
        if response.has_key('members'):
            for member_data in response['members']:
                member = Member.objects.filter(email_address=member_data['email_address'], list=m_list).first()
                if member is None:
                    member = Member()
                member.load_from_dict(member_data)
                member.list = m_list
                member.save()

    def create(self, list_id, email_address, status='subscribed'):
        response = self.mailchimp.request(self.resource,
                                          self.endpoint % list_id,
                                          'POST',
                                          data={'email_address': email_address,
                                                'status': status}, )

        print "creting %s on %s" % (response['email_address'], list_id)
        m_list = List.objects.filter(mailchimp_id=list_id).first()
        member, created = Member.objects.get_or_create(email_address=response['email_address'],
                                                       mailchimp_id=response['id'],
                                                       list=m_list,
                                                       status=response['status'],
                                                       unique_email_id=response['unique_email_id'])

        if created:
            print "MEMBER CREATED %s %s" %(member, m_list)
        else:
            print "MEMBER NOT CREATED %s" % list_id

        return member

    
class Member(BaseChimpModel):
    STATUS_CHOICE = (
        ('subscribed',_('Subscribed')),
        ('unsubscribed',_('Unsubscribed')),
        ('cleaned',_('Cleaned')),
        ('pending',_('Pending')),
    )
    email_address = models.CharField(max_length=150)
    status = models.CharField(max_length=150, choices=STATUS_CHOICE)
    mailchimp_id = models.CharField(max_length=50)
    unique_email_id = models.CharField(max_length=50)
    list = models.ForeignKey(List, null=True, blank=True)
    objects = MemberManager()

    def get_mergefield(self, name):
        mergefield = self.mergefield_set.filter(label=name).first()
        try:
            return mergefield.value
        except Exception, e:
            return None

    def set_mergefield(self, name, value):
        mergefield = self.mergefield_set.filter(label=name).first()
        if mergefield is None:
            mergefield = MergeField()
            mergefield.member = self
            mergefield.label=name

        mergefield.value=value
        mergefield.save()

        return mergefield.value

    def get_mergefield_dict(self):
        data = {}
        mergefields = self.mergefield_set.all()
        for field in mergefields:
            data[field.label] = field.value

        return data

    def get_endpoint(self):
        endpoint = super(Member, self).get_endpoint() % self.list.mailchimp_id
        return "%s/%s" % (endpoint, self.mailchimp_id)

    def load(self, data=None):
        data = self.request(method='GET')
        self.load_from_dict(data)

    def load_from_dict(self, data):
        self.email_address=data['email_address']
        self.mailchimp_id=data['id']
        self.status=data['status']
        self.unique_email_id=data['unique_email_id']
        self.save()

        for label, value in data['merge_fields'].iteritems():
            self.set_mergefield(label, value)

    def update(self):
        args = {
            'email_address': self.email_address,
            'status': self.status,
            'merge_fields': self.get_mergefield_dict()
        }
        
        self.request(args, 'PUT')

    def delete(self):
        try:
            self.request(method='DELETE')
        except Exception, e:
            pass
            
        super(Member, self).delete()

    def __unicode__(self):
        return self.email_address
        
    class Meta:
        app_label = 'mailchimp3'


class MergeField(models.Model):
    member = models.ForeignKey(Member)
    label = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.value
        
    class Meta:
        app_label = 'mailchimp3'
