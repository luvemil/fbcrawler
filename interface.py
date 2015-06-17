import facebook
import requests
import json
       

def getAllPosts(graph_list):
    array = []
    while True:
        array += [ stuff for stuff in graph_list['data'] ]
        try:
            graph_list = requests.get(graph_list['paging']['next']).json()
        except KeyError:
            break
        return array

def getFromFile(file_name):
    file = open(file_name,"r")
    posts = json.load(file)
    file.close()
    return posts

def getMessages(posts):
    """Returns all the messages in formate [ message1, ... ]"""
    messages = []
    for post in posts:
        try:
            messages.append(post['message'])
        except KeyError:
            pass
    return messages

class Session(facebook.GraphAPI):
    """Usage: 
        session = Session('my_friend_nickname',auth_token)
        wall = session.getAllPosts()
        To change page, you can do:
        session.set_node('new_page')
        wall = session.getAllPosts()
    """

    def __init__(self, page_name=None, *args, **kwargs):
        #facebook.GraphAPI.__init__(self, *args, **kwargs)
        super(Session,self).__init__(*args,**kwargs)
        self.set_node(page_name)

        # Will hold the beginning of a wall
        self.posts = None

        # WIll hold the whole wall
        self.all_posts = None

    def set_node(self, page_name):
        if not page_name:
            self.node = None
            return
        self.node = self.get_object(page_name)

    def getAllPosts(self, page_name=None):
        if not self.node:
            if not page_name:
                return []
            self.set_node(page_name)

        self.posts = self.get_connections(self.node['id'], "posts")
        self.all_posts = getAllPosts(self.posts)
        return self.all_posts
    
    def save(self, file_name):
        file = open(file_name,"w")
        json.dump(self.all_posts,file)
        file.close()

