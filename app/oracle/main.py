
#!/home/matti/IoT-Microservice/venv/bin/python3.8
# coding: utf-8

from serviceManager import execute
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    data = execute(params)
    return data


# In[ ]:



