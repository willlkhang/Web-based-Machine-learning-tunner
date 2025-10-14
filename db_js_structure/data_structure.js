db.createCollection("jobs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["epochs", "learning_rate", "batch_size"],
      properties: {
        epochs: {
          bsonType: "int",
          minimum: 1,
          maximum: 9999,
          description: "Number of epochs (>=1, <=9999)"
        },
        learning_rate: {
          bsonType: "double",
          minimum: 0,
          maximum: 1,
          description: "Learning rate between 0 and 1"
        },
        batch_size: {
          bsonType: "int",
          minimum: 1,
          description: "Batch size must be >=1"
        },
        status: {
          bsonType: "bool",
          description: "Training status: true=done, false=pending"
        },
        time_created: {
          bsonType: "date",
          description: "When the job was created"
        },
        time_finished: {
          bsonType: ["date", "null"],
          description: "When the job finished (if any)"
        },
        run_time: {
          bsonType: ["double", "null"],
          description: "Total runtime in seconds"
        },
        accuracy: {
          bsonType: ["double", "null"],
          description: "Final accuracy score"
        }
      }
    }
  }
})
