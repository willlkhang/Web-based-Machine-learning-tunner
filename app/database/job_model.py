from mongoengine import *
import datetime

class Job(Document):
    epochs = IntField(required=True, default=5, min_value=1, max_value=9999) #initialize this limit, however, the UI will raise exception if ti exceeds the defined limits.
    learning_rate = FloatField(required=True, default=0.001, min_value=0, max_value=1) #value must be in arange (0-1)
    batch_size = IntField(required=True, default=64, min_value=1) #endband deals with max value
    status = BooleanField(default=False, choices=[True, False]) #Done -> True, Pending -> false
    time_created = ComplexDateTimeField(default=datetime.datetime.now(datetime.UTC))
    time_finished = ComplexDateTimeField(default=None)
    run_time = FloatField(default=None)
    accuracy = FloatField(default=None)

    @classmethod
    def create_or_get_job(cls, epochs, learning_rate, batch_size):
        #check exist data
        job = cls.objects(epochs=epochs, learning_rate=learning_rate, batch_size=batch_size).first() #find and return the first match data of the object from the database
        if job:
            print("An Architecture of this Hyperparameter configuration is already exist")
            return "An Architecture of this Hyperparameter configuration is already exist", job
        else:
            new_job = cls(epochs=epochs, learning_rate=learning_rate, batch_size=batch_size)
            new_job.save() #save to database
            return "New Architecture created and saved", new_job
