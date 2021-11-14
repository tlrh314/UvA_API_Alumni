import datetime
import logging
import os
import pickle

import requests
import wget
from bs4 import BeautifulSoup

# TODO: check formatting, resolve initials problem for people with written out first name


def strip_title(full_name):
    possible_titles = ["prof", "dr", "ir"]
    full_name = full_name.replace(".", "").lower()
    supervisor_titles = ""

    for el in possible_titles:
        if el in full_name.lower():
            supervisor_titles += el + ". "
            full_name = full_name.replace(el, "")

    while full_name[0] == " ":
        full_name = full_name[1:]

    return supervisor_titles, full_name


def make_datetime_object(date):
    date_format_els = ["th", "st", "nd", "rd"]
    new_date = date
    for date_format_el in date_format_els:
        if new_date.split(",")[0][-2:] == date_format_el:
            new_date = " ".join([new_date.split(",")[0][:-2], new_date.split(",")[1]])
    datetime_obj = datetime.datetime.strptime(new_date, "%B %d  %Y")
    return datetime_obj


def split_name(name):
    namesplit = name.split(" ")
    initials = namesplit[0].replace(".", "")
    prefix = ""
    if namesplit[1] in ["van", "de", "den", "der"]:
        prefix += namesplit[1]
        if namesplit[2] in ["der", "den", "de"]:
            prefix += " " + namesplit[2]
            namesplit = namesplit[2:]
        else:
            namesplit = namesplit[1:]

    last_name = " ".join(namesplit[1:])
    initials = initials.upper()
    last_name = last_name[0].upper() + last_name[1:]
    return initials, prefix, last_name


logging.captureWarnings(True)


def get_persons(base_url, page, degree_type, use_headers, file_target_location):
    verify_val = True

    # Download abstract, download full pdf.
    download_abstract = True
    download_fullPdf = True
    download_profilePicture = True
    download_thesisPicture = True

    url = base_url % (10 * page + 1, degree_type)

    if "https" in url:
        verify_val = False
    if use_headers:
        headers = requests.utils.default_headers()
        headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36"  # noqa: E501
            }
        )
        r = requests.get(url, headers=headers, verify=verify_val)
    else:
        r = requests.get(url, verify=verify_val)

    # Make object
    bsObj = BeautifulSoup(r.content, "html.parser")

    # Find general entries
    res_top = bsObj.findAll("table", {"border": "1"})

    # Check if there are any results
    if len(res_top) > 0:
        has_results = True
    else:
        has_results = False

    result_list = []
    if has_results:
        # to store each record
        record_set = []
        api_record_set = []

        # pick each 3 tables and combine them
        for i in range(int(len(res_top) / 3.0)):
            sub_record_set = [res_top[i * 3], res_top[i * 3 + 1], res_top[i * 3 + 2]]
            record_set.append(sub_record_set)

        # filter the records on if they contain api:
        for i in record_set:
            api_record = False
            for j in i:
                if "API" in str(j):
                    api_record = True

            if api_record is True:
                api_record_set.append(i)

        # Per record in api_record set we have 3 sub entries:
        # in the first the information about the name, institute, date etc etc is stored
        # in the second the information about the thesis itself is stored
        # in the third the information aobut the location of the thesis is stored.

        for j in range(len(api_record_set)):
            # Retrieve the individual tables again.
            first_contents = api_record_set[j][0].findAll("td")
            second_contents = api_record_set[j][1].findAll("td")
            third_contents = api_record_set[j][2].findAll("td")

            # First_info
            name_el = first_contents[0]
            master_program_el = first_contents[1]
            date_el = first_contents[2]
            research_group_el = first_contents[4]
            supervisor_el = first_contents[6]

            # format the info
            name = name_el.find("span").text.split("</b>")[0].strip("\t\n\r")

            try:
                master_program = master_program_el.find("a").text.split("</a>")[0]
            except AttributeError:
                # print master_program_el
                master_program = (
                    master_program_el.text.split("</td>")[0]
                    .split(":")[1]
                    .strip(" \t\n\r")[0:]
                )

            date = date_el.text.split("</td>")[0].strip("\t\n\r")
            research_group = (
                research_group_el.text.split("</td>")[0]
                .split(":")[1]
                .strip("\t\n\r")[1:]
            )
            supervisor = (
                supervisor_el.text.split("</td>")[0].split(":")[1].strip("\t\n\r")[1:]
            )

            # Second_info
            # Sometimes, no profile picture is present, so we count backwards and try it
            try:
                profilePicture_el = second_contents[-3]
                profilePicture_link = profilePicture_el.find("img")["src"]
            except IndexError:
                profilePicture_link = ""

            description_el = second_contents[-2]
            thesisPicture_el = second_contents[-1]

            # format the info
            thesis_title = (
                description_el.find("strong").text.split("</strong>")[0].strip("\t\n\r")
            )
            description_text = (
                str(description_el)
                .split("</td>")[-2]
                .split("<br/>")[-1]
                .strip("\n\t\r")
            )
            thesisPicture_link = thesisPicture_el.find("img")["src"]

            # Third info
            theses_els = third_contents[0].findAll("a")

            # format the info
            # Sometimes, no abstract is present, so first we test, and
            # count backwards in order to be able to get it if present
            abstract_index = None
            fulltext_index = -1

            for k in range(len(theses_els)):
                if "Scientific abstract" in str(theses_els[k]):
                    abstract_index = -2

            abstract_link = ""
            if abstract_index is not None:
                abstract_el = theses_els[abstract_index]
                abstract_link = abstract_el["href"]

            fulltext_link = ""
            fulltext_mail = ""

            if fulltext_index is not None:
                fulltext_el = theses_els[fulltext_index]
                fulltext_temp = fulltext_el["href"]
                if "https" in fulltext_temp:
                    fulltext_link = fulltext_temp
                elif "mailto" in fulltext_temp:
                    fulltext_mail = fulltext_temp.split(":")[-1][:-1]
                else:
                    fulltext_mail = fulltext_el["href"]

            not_found_name = ""

            local_fulltext_location = not_found_name
            local_abstract_location = not_found_name
            local_profilepicture_location = not_found_name
            local_thesispicture_location = not_found_name

            if download_abstract:
                if abstract_link != not_found_name:
                    abstract_filename = abstract_link.split("/")[-1]
                    target_filename_full = str(file_target_location + abstract_filename)
                    if not os.path.exists(target_filename_full):
                        downloaded_filename = wget.download(
                            abstract_link, out=target_filename_full
                        )
                        if os.path.exists(target_filename_full):
                            local_abstract_location = target_filename_full
                    else:
                        local_abstract_location = target_filename_full

            if download_fullPdf:
                if not fulltext_link == not_found_name:
                    fulltext_filename = fulltext_link.split("/")[-1]
                    target_filename_full = str(file_target_location + fulltext_filename)
                    if not os.path.exists(target_filename_full):
                        downloaded_filename = wget.download(
                            fulltext_link, out=target_filename_full
                        )
                        if os.path.exists(target_filename_full):
                            local_fulltext_location = target_filename_full
                    else:
                        local_fulltext_location = target_filename_full

            if download_profilePicture:
                if not profilePicture_link == not_found_name:
                    profilePicture_filename = profilePicture_link.split("/")[-1]
                    target_filename_full = str(
                        file_target_location + profilePicture_filename
                    )
                    if not os.path.exists(target_filename_full):
                        downloaded_filename = wget.download(
                            profilePicture_link, out=target_filename_full
                        )
                        if os.path.exists(target_filename_full):
                            local_profilepicture_location = target_filename_full
                    else:
                        local_profilepicture_location = target_filename_full

            if download_thesisPicture:
                if not thesisPicture_link == not_found_name:
                    thesispicture_filename = thesisPicture_link.split("/")[-1]
                    target_filename_full = str(
                        file_target_location + thesispicture_filename
                    )
                    if not os.path.exists(target_filename_full):
                        downloaded_filename = wget.download(  # noqa: F841
                            thesisPicture_link, out=target_filename_full
                        )
                        if os.path.exists(target_filename_full):
                            local_thesispicture_location = target_filename_full
                    else:
                        local_thesispicture_location = target_filename_full

            sub_dict = {}

            print("name = %s" % name)
            sub_dict["name"] = name

            # TODO if full first name is used, then think of a way to get that, instead of thinking those are initials
            author_initials, author_prefix, author_last_name = split_name(name)

            print("author_initials = %s" % author_initials)
            sub_dict["author_initials"] = author_initials
            print("author_prefix = %s" % author_prefix)
            sub_dict["author_prefix"] = author_prefix
            print("author_last_name = %s" % author_last_name)
            sub_dict["author_last_name"] = author_last_name
            print("degree_type = %s" % degree_type)
            sub_dict["degree_type"] = degree_type
            print("master_program = %s" % master_program)
            sub_dict["program"] = master_program
            print("research_group = %s" % research_group)
            sub_dict["research_group"] = research_group

            print("supervisor = %s" % supervisor)
            sub_dict["supervisor"] = supervisor

            supervisor_full = supervisor
            supervisor_titles, supervisor_name = strip_title(supervisor_full)
            supervisor_initials, supervisor_prefix, supervisor_last_name = split_name(
                supervisor_name
            )

            print("supervisor_titles = %s" % supervisor_titles)
            sub_dict["supervisor_titles"] = supervisor_titles
            print("supervisor_initials = %s" % supervisor_initials)
            sub_dict["supervisor_initials"] = supervisor_initials
            print("supervisor_prefix = %s" % supervisor_prefix)
            sub_dict["supervisor_prefix"] = supervisor_prefix
            print("supervisor_last_name = %s" % supervisor_last_name)
            sub_dict["supervisor_last_name"] = supervisor_last_name

            print("date = %s" % date)
            sub_dict["date"] = date

            print("thesis_title = %s" % thesis_title)
            sub_dict["thesis_title"] = thesis_title
            print("description_text = %s" % description_text)
            sub_dict["description_text"] = description_text
            print("profilePicture_link = %s" % profilePicture_link)
            sub_dict["profilepicture_link"] = profilePicture_link
            print("thesisPicture_link = %s" % thesisPicture_link)
            sub_dict["thesispicture_link"] = thesisPicture_link
            print("Fulltext_link = %s" % fulltext_link)
            sub_dict["fulltext_link"] = fulltext_link
            print("Fulltext_mail = %s" % fulltext_mail)
            sub_dict["fulltext_mail"] = fulltext_mail
            print("Abstract_link = %s" % abstract_link)
            sub_dict["abstract_link"] = abstract_link
            print("Local_abstract_location = %s" % local_abstract_location)
            sub_dict["local_abstract_location"] = local_abstract_location
            print("Local_fulltext_location = %s" % local_fulltext_location)
            sub_dict["local_fulltext_location"] = local_fulltext_location
            print("Local_profilepicture_location = %s" % local_profilepicture_location)
            sub_dict["local_profilepicture_location"] = local_profilepicture_location
            print("local_thesispicture_location = %s" % local_thesispicture_location)
            sub_dict["local_thesispicture_location"] = local_thesispicture_location
            print("\n")

            result_list.append(sub_dict)
            print(sub_dict)

    return has_results, result_list


def loop_over(file_target_location):
    i = 0
    has_results = True
    degree_type = "master"  # Either choose master or bachelor
    grand_result_list = []

    # Create the location where the downloaded files are stored, if necessary
    if not os.path.isdir(file_target_location):
        print("directory not present yet, making now")
        os.mkdir(file_target_location, "0755")
        if os.path.isdir(file_target_location):
            print("Succesfully created target directory")

    while has_results is True:
        # base_url = 'https://esc.fnwi.uva.nl/thesis/apart/phys/thesis.php?page=phys&start=%d&level=%s'%(10*i+1, degree)
        base_url = "https://esc.fnwi.uva.nl/thesis/apart/phys/thesis.php?page=phys&start=%d&level=%s"

        # Check wether there are any results, and extract them
        has_results, sub_result_list = get_persons(
            base_url, i, degree_type, True, file_target_location
        )

        # Store the results of the 1 page scan in the master list
        for entry in sub_result_list:
            grand_result_list.append(entry)

        i += 1
    pickle.dump(
        grand_result_list, open(file_target_location + "grand_result_list.dump", "wb")
    )
    # print(str(grand_result_list))


if __name__ == "__main__":
    output_dir = "./scraped_theses/"
    loop_over(output_dir)

    # base_url = "https://esc.fnwi.uva.nl/thesis/apart/phys/thesis.php?page=phys&start="
    # get_persons(base_url+'%d&level=%s', 0, 'master', True, '../results/')
    # get_persons(base_url+'%d&level=%s', 1, 'master', True, output_dir)
    # get_persons(base_url+'%d&level=%s', 2, 'master', True, output_dir)
    # get_persons(base_url+'%d&level=%s', 3, 'master', True, output_dir)
