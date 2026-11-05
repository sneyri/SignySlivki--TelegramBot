from itdpy import ITDClient
from itdpy.exceptions import NotFoundError

client = ITDClient(refresh_token="token")

users = client.users
posts = client.posts
comments = client.comments
search = client.search

POST_ID = '2bedc019-0d3c-4e66-8148-8ec208c09c1f'

def checkPost(postId):
    try:
        post = posts.get(postId)

        if '#сигнысливки' in post.content.lower():
            return True
        else:
            return False
    except NotFoundError:
        return
    except:
        return

def findCode(username, code):
    code = code.lower().strip()
    
    comment_list = comments.list_all(POST_ID)
    
    for comment in comment_list:
        comment_user = comment.author.username
        comment_content = comment.content.lower().strip()
        
        if username == comment_user and comment_content == code:
            return True
    
    return False

def searchUsers(username: str):
    if not username or not username.strip():
        return []
    
    try:
        results = search.users(username)
        return results if results else []
    except:
        return []

def searchByDisplayName(display_name: str):
    if not display_name or not display_name.strip():
        return []
    
    try:
        results = search.users(display_name)

        matched_users = []
        for user in results:
            if hasattr(user, 'display_name') and display_name.lower() in user.display_name.lower():
                matched_users.append(user)
            elif hasattr(user, 'username') and display_name.lower() in user.username.lower():
                matched_users.append(user)
        return matched_users
    except:
        return []

def getUser(username: str):
    if not username or not username.strip():
        return None
    
    username = username.strip()
    
    if username.startswith('@'):
        username = username[1:]

    try:
        found_user = users.get(username)
        return [found_user] if found_user else []
    except NotFoundError:
        return []
    except:
        return []

def getUsers(search_query: str):
    if not search_query or not search_query.strip():
        return []
    
    search_query = search_query.strip()
    
    if search_query.startswith('@'):
        search_query = search_query[1:]
    
    all_users = []
    seen_usernames = set()
    
    exact_user = getUser(search_query)
    if exact_user:
        for user in exact_user:
            username = getattr(user, 'username', '')
            if username and username not in seen_usernames:
                all_users.append(user)
                seen_usernames.add(username)
    
    search_results = searchUsers(search_query)
    if search_results:
        for user in search_results:
            username = getattr(user, 'username', '')
            if username and username not in seen_usernames:
                all_users.append(user)
                seen_usernames.add(username)
    
    display_results = searchByDisplayName(search_query)
    if display_results:
        for user in display_results:
            username = getattr(user, 'username', '')
            if username and username not in seen_usernames:
                all_users.append(user)
                seen_usernames.add(username)
    
    unique_users = []
    seen = set()
    for user in all_users:
        user_id = getattr(user, 'id', None) or getattr(user, 'username', '')
        if user_id and user_id not in seen:
            unique_users.append(user)
            seen.add(user_id)
    
    return unique_users
