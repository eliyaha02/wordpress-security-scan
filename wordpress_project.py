import requests
from art import *

def welcome():
    """
    Prints the entry banner for the tool and url global var
    """
    tprint("WordPress   security")
    print("    author: @EliyaLahav, version: 1.0.0")
    print("""
    
    """)
    global url
    url = input("Insert the URL (Like https://example.com): ")


def discovery_version():
    """
    discovery the wordpress version by the generator line of the source code
    :return: if the generator line is visible or not
    """
    print("-------------------------------------------------------")
    source_code = requests.get(url).text
    generator = source_code.find("generator")

    if generator != -1:
        generator_to_end = source_code[generator:]
        find_wordpress = generator_to_end.find("WordPress")
        find_wordpress_tow = generator_to_end.find("/>")
        print("your generator line no hidden. This is a wordpress system, version " + generator_to_end[find_wordpress:find_wordpress_tow - 2])
    else:
        find_wp = source_code.find("wp-")
        if find_wp == -1:
            print("We'm sorry, but we were unable to identify this wordpress system")
            return False
        else:
            print("your generator line is hidden. well done!")
    print("-------------------------------------------------------")


def https_and_hsts():
    """
    Checks if the website uses https and if so, does it also use htsts
    """
    find_https = url.find("://")
    rest_url = url[find_https:]
    http_url = "{0}{1}{2}".format("http", rest_url, "/")
    check_https = requests.get("{0}{1}".format("https",rest_url))
    status_code = check_https.status_code

    if (url[find_https-1] == check_https.url[find_https-1]) or (str(status_code) == "200"):
        http_request = requests.get(http_url)
        if http_request.url == http_url:
            print("Your website uses https, but not hsts. it's bad!")
        else:
            print("Your website uses https and hsts. very good!")
    else:
        print("Your website not uses https. it's very bad!")
    print("-------------------------------------------------------")


def search_important_headers():
    """
    Checks if the website uses important headers
    """
    list_important_headers = ['X-Frame-Options', 'Referrer-Policy', 'Permissions-Policy',
                              'X-XSS-Protection', 'Strict-Transport-Security', 'X-Content-Type-Options']
    list_headers_not_defined = []
    http_request = requests.get(url)
    list_headers = http_request.headers
    for header in list_important_headers:
        if header not in list_headers:
            list_headers_not_defined.append(header)
    if len(list_headers_not_defined) > 0:
        print("You need to define the following headers: {0}".format(list_headers_not_defined))
    else:
        print("All headers are defined. very good work!")
    print("-------------------------------------------------------")


def discovery_admin_panel():
    """
    Checks whether admin panel is visible or not
    """
    admin_panel = "/wp-admin"
    website = requests.get("{0}{1}".format(url,admin_panel))
    if website.status_code == 200:
        print("Your admin panel is visible. it's bad!")
    else:
        print("Your admin panel is hidden. Well done!")
    print("-------------------------------------------------------")


def discovery_wordpress_with_robots_file():
    """
    Checks if the robots.txt file reveals that it is a wordpress system
    """
    robots = "/robots.txt"
    http_request = requests.get("{0}{1}".format(url,robots))
    if http_request.status_code == 200:
        find_wp = http_request.text.find("wp-")
        if find_wp != -1:
            print("The robots.txt file reveals that your system is wordpress")
        else:
            print("The robots.txt file reveals that your system is wordpress")
    print("-------------------------------------------------------")
    print("")



def discovery_usernames_with_author_query():
    """
    Checks if the author query returns usernames or is blocked
    """
    author = "/?author="
    number_of_users = input("We will perform an author query. Enter the number of usernames we will scan: ")

    list_of_users = []
    for number in range(int(number_of_users)):
        if number == 0:
            continue
        url_author = requests.get("{0}{1}{2}".format(url, author, number))
        result = url_author.url
        if url != result:
            if url_author.status_code == 404:
                continue
            find_username = result.rfind("author/")
            list_of_users.append(result[find_username + len("author/"):-1])
        else:
            print("Excellent! Author query blocked!")
            break
        print("The author query was not blocked. Usernames found: " + "".join(list_of_users))
    print("-------------------------------------------------------")


def discovery_users_with_wp_json():
    """
    Checks if wp-json returns usernames or is blocked
    """
    list_of_users = []
    syntax_wp_json = "/wp-json/wp/v2/users"
    request_wp_json = requests.get("{0}{1}".format(url, syntax_wp_json)).text
    find_users = request_wp_json.find("name")
    if find_users != -1:
        lines = request_wp_json.split("url")
        for line in lines:
            find_name = line.find("name")
            if find_name != -1:
                cut_from = find_name+len("name")+3
                cut_to = line.rfind(",")-1
                username = line[cut_from:cut_to]
                list_of_users.append(username)
        print("The wp-json is not blocked. Usernames found: {0}".format("".join(list_of_users)))
    else:
        print("The wp-json has been blocked. good work!")
    print("-------------------------------------------------------")


def checker_xmlrpc():
    """
    Checks if xmlrpc.php is open or blocked
    """
    xmlrpc = "/xmlrpc.php"
    https_request = requests.get("{0}{1}".format(url, xmlrpc))
    if https_request.status_code == 405:
        print("xml-rpc is not disabled. it's bad!")
    else:
        print("xml-rpc is disabled. well done!")
    print("-------------------------------------------------------")


def find_exposed_folders():
    """
    Checks if there are wordpress folders that are visible to everyone
    """
    folders = ["/wp-content/uploads", "/wp-includes", "/.git"]
    list_of_exposed_folders = []
    for folder in folders:
        get_folder = requests.get("{0}{1}".format(url, folder))
        if get_folder.status_code == 200:
            list_of_exposed_folders.append("{0}{1}".format(folder, ", "))
    if len(list_of_exposed_folders) > 0:
        print("The folders found: {0}".format("".join(list_of_exposed_folders)) + ". it's bad!")
    else:
        print("No exposed folders found. good work!")
    print("-------------------------------------------------------")


def discovery_plugins():
    """
    Searches for plugins installed on the wordpress site,
     by searching the readme.txt file. The search is only on the 36 most vulnerable and important plugins
    """
    list_of_plugins = ["elementor", "wordfenc", "wp-hide-security-hardening", "wp-sri", "wpforms-lite",
                       "wps-hide-login", "litespeed-cache", "comment-from-csrf-protection", "all-in-one-wp-mugration",
                       "gutenberg", "woocommerce", "ultimate-member", "yoast-seo", "ninja-Forms", "nextgen gallery",
                       "jetPack", "all-in-one-seo-pack", "contact-form-7", "patch-for-revolution-slider",
                       "gravity-Forms",
                       "timthumb", "wp-symposium-pro", "wptf-image-Gallery", "google-mp3-audio-player",
                       "wp-database-backup",
                       "wp-e-commerce-shop-styling", "candidate-application-Form", "wp-Mobile-Detector",
                       "ajax-pagination",
                       "newsletter", "google-photos-gallery", "tinymce-thumbnail-gallery", "dukapress",
                       "wp-file-manager",
                       "history-collection", "work-the-flow-file-upload"]
    list_of_plugins_found = []
    url_plugins = "{0}{1}".format(url, "/wp-content/plugins/")
    readme = "/readme.txt"

    if requests.get(url_plugins).status_code == 200:
        for plugin in list_of_plugins:
            get_readme = requests.get("{0}{1}{2}".format(url_plugins, plugin, readme))
            status_code = get_readme.status_code
            if status_code != 404:
                list_of_plugins_found.append(plugin)

        if len(list_of_plugins_found) < 1:
            print("No plugins found")
        else:
            print("plugins found: {0}".format(list_of_plugins_found))

            for plugin in list_of_plugins_found:
                plugin_get = requests.get("{0}{1}{2}".format(url_plugins, plugin, readme))
                find_changelog = plugin_get.text.rfind("Changelog")
                if find_changelog == -1:
                    find_changelog = plugin_get.text.rfind("Change")
                output = plugin_get.text[find_changelog:find_changelog + 30]
                find_version_one = output.find(".")
                find_version_two = output.rfind(".")
                print("{0}, version {1}".format(plugin, output[find_version_one - 2:find_version_two + 2]))
    else:
        print("We are sorry, but we were unable to identify the system as a wordpress system")
    print("-------------------------------------------------------")
    print("finish!")

   
