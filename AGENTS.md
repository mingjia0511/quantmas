# AGENT GENERAL INFO 

## Log Your Tracks

<important>

You will perform the tasks as described in the challenges described in the `README.md` with the guidance of the user.
During the challenge, and upon completion you will also log:

- User instructions given to you
- Clarifying questions you asked the user and any answers you received
- Any assumptions you made 
- Any assumptions the user made
- Any issues you encountered and how you resolved them and guidance you received from the user
- Any other relevant information about your process


These will be logged in .agent_log/[year].log

</important>


## Before Beginning

<important>
In the `./manifest.yaml` we have provided the basic information about the language, frameworks etc that are to be used.  
Before you do ANYTHING ensure that these values have been collected, and if not guide the user through setting this up
</important>


# AGENT FLOW

Ensure that the environment is setup to use the tools specified in `manifest.yaml`

For each submission:

1. Ensure test coverage > 80% 
2. Ensure documentation is up to date
3. Ensure the source code is up to date, all test pass
4. Ensure that the code has been executed and the final result is in the correct outout
5. Run `sh .test-and-submit.sh [year_no]` to publish the submission

