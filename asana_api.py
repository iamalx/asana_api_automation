import asana
import time

print(asana)
# replace with your personal access token. 
personal_access_token = ''

# Construct an Asana client
client = asana.Client.access_token(personal_access_token)

# # Get your user info
me = client.users.me()
print('results', me)
# # Print out your information
#print("Hello world! " + "My name is " + me['name'] + "!")

workplace = client.workspaces.get_workspaces({}, opt_pretty=True)
workplace_gid = list(workplace)[0]['gid']

# w_tags = client.tags.get_tags_for_workspace(workplace_gid, {}, opt_pretty=True)
# print('w_tags', list(w_tags))

tags_gids = {
    'social_ads': '1199364787586733',
    'social_posts': '1199364787586735',
    'gads': '1199364787586740',
    'rw': '1199364787586734',
    'blog': '1199364787586739',
    'seo': '1199364787586741',     
}

duplicate_params = {
    "include": [
        "notes",
        "assignee",
        'subtasks',
        'followers',
        # 'projects',
        'dates',
    ],
    "name": '',   
}

substasks_dates = {
    'social_ads': [{"due_on": "2021-01-28", "completed": False}],
    'social_posts': [{"due_on": "2021-01-28", "completed": False, "assignee": "12345"}, {"due_on": "2021-02-12", "completed": False, "assignee": "12345"}],
    'gads': [{"due_on": "2020-01-30", "completed": False}],
    'rw': [{"due_on": "2021-02-01", "completed": False,  "assignee": "12345"}],
    'blog': [{"due_on": "2020-12-30", "completed": False}],
    'seo': {"due_on": "2021-01-31", "completed": False},     
}

# '1198740358621275'
project_lists = [
    {'gid': '904221851811454', 'name': 'Ablantis | Cortadi'},
    {'gid': '904221851811463', 'name': 'Skeens Family Dentistry | Skeens'}  ,   
    {'gid': '905386446845289', 'name': 'Dr. Greg Campbell |'},
    # {'gid': '1120799747616556', 'name': 'North Brand | Acopian'},
    {'gid': '1126165252248492', 'name': 'DeAngelis Family Dentistry |'}  ,      
    {'gid': '1140179551070941', 'name': 'Ivory Pointe | Miller'},
    {'gid': '1144012943937515', 'name': 'Arvada Dental | Bennett'},
    {'gid': '1149065215204115', 'name': 'RB Dental Excellence | Lozano'},       
    {'gid': '1158659078123146', 'name': 'All Smiles | Fatourachi'},
    {'gid': '1151404834337091', 'name': 'Cassell Dentistry | Cassell'},
    # {'gid': '1156864821551628', 'name': 'Moonlight | Vane'},
    # {'gid': '1177715618432778', 'name': 'Palisades | Kryzman '},
    {'gid': '1164801455469347', 'name': 'William V. Carlo | Carlo'},
    {'gid': '1166534229277406', 'name': 'Altrock Fabb Dental |'},
    {'gid': '1180663333207442', 'name': 'WoodCreek | Wygant'},
    {'gid': '1181499572475162', 'name': 'Fifth Ave. | Mojaver'},
    {'gid': '1188586386435378', 'name': 'Talentscale | Doug Poldrugo'},
    # {'gid': '1190431369643804', 'name': 'Park Smiles | Byrnes'},
    {'gid': '1192200120142468', 'name': 'Landmark Dental | Berry'},
    # {'gid': '1198159986322778', 'name': 'Harmony | Farid'},
    {'gid': '1198882559175104', 'name': 'Kids City Dental | McFarlin'},
    # {'gid': '1199677041876246', 'name': 'Art of Pediatric | Ong'},
    # {'gid': '1199677041876248', 'name': 'Scripps West Dental | Tasto'},
    # {'gid': '1199677041876250', 'name': 'Torrey Hills Dental |Tasto'},
    # {'gid': '1199691976812695', 'name': 'AMS | Saad'},
    # {'gid': '1199520769738551', 'name': 'Dream Team Dental | NimaKevin'},       
    # {'gid': '1195153983694026', 'name': 'Solstice | Manning'},
    # {'gid': '1161919964938722', 'name': 'Sycamore Dental | Sarkaria & Englert'},
    # {'gid': '1181499572475171', 'name': 'Enlighten | Blackwell'},
    # {'gid': '1188728043259814', 'name': 'Hercules | Teodoro'},
]

tasks_type = 'seo'
new_month = ' February'

def get_projects():
    ## gets project from worksplace and filter it 
    
    result = client.projects.get_projects_for_workspace(workplace_gid, {}, opt_pretty=True)
    
    for item in result: 
        if item['name'].find('|') != -1 and item['name'].find('Onboarding') == -1:
            item.pop('resource_type', None)
            # print(item)

# get_projects()

def duplicate_template_tasks():
    ## duplicate task from temaplate

    tasks = client.tasks.get_tasks_for_tag(tags_gids[tasks_type], {}, opt_pretty=True)
    tasks_ls = list(tasks)
    
    count_task = 0    
    
    ## duplicate tasks and edit them
    for i, item in enumerate(project_lists):
        ## duplicate tasks
        duplicate_params['name'] =  item['name'].split('|', 1)[0] + tasks_ls[0]['name'].split(' ', 1)[1] .rsplit(' ', 1)[0]  + new_month
        duplicate_new_task = client.tasks.duplicate_task(tasks_ls[0]['gid'], duplicate_params, opt_pretty=True)
        
        ## get sections  
        section = client.sections.get_sections_for_project(item['gid'], {}, opt_pretty=True)
        section_ls = list(section)
        
        ## find blog sections and get gid
        blog_section_gid = ''

        for i, item in enumerate(section_ls):
            if item['name'] == 'Blogs':
                blog_section_gid = item['gid']

        ## add task to section
        section_update = client.sections.add_task_for_section(blog_section_gid, {'task': duplicate_new_task['new_task']['gid']}, opt_pretty=True)
        
        count_task += 1

# duplicate_template_tasks()

def update_subtasks(duplicate_new_task, new_task_data):
    ## get old subtaks
    new_susbtasks = client.tasks.get_subtasks_for_task(duplicate_new_task['new_task']['gid'], {}, opt_pretty=True) 
    new_susbtasks_ls =  list(new_susbtasks)

    ## update substask
    for i, subtask in enumerate(substasks_dates[tasks_type]):
        substasks_dates[tasks_type][i]['assignee'] = new_task_data['assignee']['gid']  
        update_sub_task = client.tasks.update_task(new_susbtasks_ls[i]['gid'], subtask, opt_pretty=True)

    print('update_subtasks', update_sub_task['gid'])

def update_tasks(duplicate_new_task):
    if tasks_type == 'seo': 
            ##  update seo tasks ||seo has no subtasks
            update_task = client.tasks.update_task(duplicate_new_task['new_task']['gid'], substasks_dates[tasks_type], opt_pretty=True)
    else:
        ## update other tasks 
        new_task_data = client.tasks.get_task(duplicate_new_task['new_task']['gid'], {}, opt_pretty=True)
        update_task = client.tasks.update_task(duplicate_new_task['new_task']['gid'], {'completed': False}, opt_pretty=True)
        time.sleep(4)
        
        ## update substask
        update_subtasks(duplicate_new_task, new_task_data)


def duplicate_old_tasks():
    ## duplicate task from old task 

    count_task = 0    
    
    ## get tasks from gids
    g_ads_tasks = client.tasks.get_tasks_for_tag(tags_gids[tasks_type], {}, opt_pretty=True)
    g_ads_tasks_ls = list(g_ads_tasks)

    for task in g_ads_tasks_ls:
        ## duplicate tasks
        duplicate_params['name'] =  task['name'].rsplit(' ', 1)[0]  + new_month
        duplicate_new_task = client.tasks.duplicate_task(task['gid'], duplicate_params, opt_pretty=True)
        
        count_task += 1
        ## update tasks and update substask
        update_tasks(duplicate_new_task)

        print('iteration:', count_task) 
    print('done', count_task) 

duplicate_old_tasks()


# def duplicate_social_ads_funct():

#     social_ads_tasks = client.tasks.get_tasks_for_tag(tags_gids['social_ads_tag'], {}, opt_pretty=True)
#     social_ads_tasks_ls = list(social_ads_tasks)
#     print('tasks: ', social_ads_tasks_ls)

#     for task in social_ads_tasks_ls:
#         duplicate_params['data']['name'] = task['name']
#         # print( duplicate_params)
#         duplicate_social_ads = client.tasks.duplicate_task(social_ads_tasks_ls[0]['gid'], duplicate_params, opt_pretty=True)
#     print('duplicate: ', duplicate_social_ads)

# duplicate_social_ads_funct()

