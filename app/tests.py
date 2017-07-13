from django.test import TestCase

# Create your tests here.
import asyncio
import time

@asyncio.coroutine
def s1(v1):

    time.sleep(1)
    print("s1>>>>>",v1)

@asyncio.coroutine
def s2(v2):

    time.sleep(2)
    print("s2>>>>>", v2)

loop = asyncio.get_event_loop()
tasks = [s1("s1"), s2("s2")]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()