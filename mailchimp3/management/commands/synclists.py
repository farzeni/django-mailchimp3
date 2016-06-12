from django.core.management import BaseCommand
from optparse import make_option
from mailchimp3.models import *


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print "Loading lists"
        m_lists = List.objects.load()
        lists = List.objects.all()

        for m_list in lists:
            print "Sync list: %s" % m_list.name
            Member.objects.load(m_list.mailchimp_id)

        print 'Done'