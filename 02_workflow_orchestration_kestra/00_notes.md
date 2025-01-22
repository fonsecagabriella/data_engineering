# Data Orchestration

<img src="../images/kestra.png" width="80%">
<br>

## Kestra

Kestra is a modern and scalable workflow orchestrator that allows you to define and run workflows with ease. It is built to be simple to use, yet scalable and performant. Kestra is fully open-source and can be used on-premise or in the cloud.

- [Beginner Tutorial List](https://www.youtube.com/watch?v=HR47SY2RkPQ&list=PLEK3H8YwZn1oaSNybGnIfO03KC_jQVChL&ab_channel=Kestra)

- [Kestra with Docker](https://www.youtube.com/watch?v=SGL8ywf3OJQ&ab_channel=Kestra)

### Flows

Flows are workflows.
Declared in yaml. 

- **id:** name of your flow
- **namespace:** environment of your flow
- **tasks:** what you want to do

### Extra concepts

- **Inputs**: Act like constant variables
````
inputs:
    - id: variable_name
    type: STRING
    defaults: example_string
````
- **Outputs:** Can be reused
- **Triggers:** Flows are executed by triggers

