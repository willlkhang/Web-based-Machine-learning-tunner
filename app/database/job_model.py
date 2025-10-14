from mongoengine import *
import datetime

class Job(Document):
    epochs = IntField(required=True, default=5, min_value=1, max_value=9999) #initialize this limit, however, the UI will raise exception if ti exceeds the defined limits.
    learning_rate = FloatField(required=True, default=0.001, min_value=0, min_value=1) #value must be in arange (0-1)
    batch_size = IntField(required=True, default=64, min_value=1) #endband deals with max value
    status = BooleanField(default=False, choices=[True, False]) #Done -> True, Pending -> false
    time_created = ComplexDateTimeField(default=datetime.datetime.now(datetime.UTC))
    time_finished = ComplexDateTimeField(default=None)
    run_time = FloatField(default=None)
    accuracy = FloatField(default=None)

