from wordpress_project import *


def main():
    welcome()

    if discovery_version() == False:
        print("finish!")

    else:
        https_and_hsts()
        search_important_headers()
        discovery_admin_panel()
        discovery_wordpress_with_robots_file()
        discovery_usernames_with_author_query()
        discovery_users_with_wp_json()
        checker_xmlrpc()
        find_exposed_folders()
        discovery_plugins()


if __name__ == '__main__':
    try:
        main()
    except:
        print("There is a problem. Try again!")
