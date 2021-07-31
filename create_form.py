import pandas as pd
import requests as req
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TYPEFORM_TOKEN')

headers = { "Authorization": f"Bearer {TOKEN}", "Accept": "application/json" }
main_url = "https://api.typeform.com"

# Создание формы

def setGetRequest(url):
    r = req.get(f"{main_url}/{url}", headers=headers)

    if (r.status_code == req.codes.ok):
        return r.json()
    
    return False

# Получение WorkSpace
def getIdFirstWorkspace():
    
    workspaces = setGetRequest("workspaces")
    if (not workspaces):
        return False

    return workspaces["items"][0]["id"]

def getDataFromExcel():
    xlsx = pd.ExcelFile("uploads/file.xlsx")
    data = pd.read_excel(xlsx, 0, header=None, keep_default_na=False)

    
    row_logic = 1
    row_que_order = 2
    row_utm = 3
    row_random = 4
    row_multy_select = 5
    row_required = 6
    row_que_type = 7
    row_type_data = 8
    row_start_data = 9

    form_name = data[0][0]

    return_dict = {
        'form_name': form_name,
        'arr_logic': [], 
        'arr_que_order': [], 
        'arr_utm': [], 
        'arr_random': [], 
        'arr_multy_select': [], 
        'arr_required': [], 
        'arr_que_type': [], 
        'arr_type_data': [], 
        'arr_data': [], 
    }

    for i in range(1, len(data.columns)):
        return_dict['arr_logic'].append(data[i][row_logic])
        return_dict['arr_que_order'].append(data[i][row_que_order])
        return_dict['arr_utm'].append(data[i][row_utm])
        return_dict['arr_random'].append(data[i][row_random])
        return_dict['arr_multy_select'].append(data[i][row_multy_select])
        return_dict['arr_required'].append(data[i][row_required])
        return_dict['arr_que_type'].append(data[i][row_que_type])
        return_dict['arr_type_data'].append(data[i][row_type_data])
        
        arr_col_data = []
        for x in range(row_start_data, len(data)):
            text = data[i][x]
            if text:
                arr_col_data.append(data[i][x])
        
        return_dict['arr_data'].append(arr_col_data)

    
    return return_dict

def setQuestionForParams(ref, title, description, required_status, choices_arr, allow_multiple_selection, randomize, type_field):

    button_text = 'Далее'

    if str(required_status).lower() == 'да':
        required_status = True
    else:
        required_status = False

    if str(allow_multiple_selection).lower() == 'да':
        allow_multiple_selection = True
    else:
        allow_multiple_selection = False
    
    if str(randomize).lower() == 'да':
        randomize = True
    else:
        randomize = False

    fields = {
        "Date": {
            "ref": ref,
            "title": title,
            "type": "date",
            "properties": {
                "description": description,
                "structure": "DDMMYYYY",
                "separator": "-"
            },
            "validations": {
                "required": required_status
            }
        },
        "Dropdown": {
            "ref": ref,
            "title": title,
            "type": "dropdown",
            "properties": {
                "description": description,
                "alphabetical_order": False,
                "randomize": randomize,
                "choices": choices_arr
            },
            "validations": {
                "required": required_status
            },
            "layout": {
                "type": "float",
                "placement": "right"
            }
        },
        "Email": {
            "ref": ref,
            "title": title,
            "type": "email",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status
            }
        },
        "File Upload": {
            "ref": ref,
            "title": title,
            "type": "file_upload",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status
            }
        },
        "Legal": {
            "ref": ref,
            "title": title,
            "type": "legal",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status
            }
        },
        "Long Text": {
            "ref": ref,
            "title": title,
            "type": "long_text",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status,
                "max_length": 20
            },
            "layout": {
                "type": "wallpaper"
            }
        },
        "Multiple Choice": {
            "ref": ref,
            "title": title,
            "type": "multiple_choice",
            "properties": {
                "description": description,
                "randomize": randomize,
                "allow_multiple_selection": allow_multiple_selection,
                "allow_other_choice": False,
                "vertical_alignment": True,
                "choices": choices_arr
            },
            "validations": {
                "required": required_status
            }
        },
        "Ranking": {
            "ref": ref,
            "title": title,
            "type": "ranking",
            "properties": {
                "description": description,
                "randomize": randomize,
                "allow_multiple_selection": allow_multiple_selection,
                "choices": choices_arr
            },
            "validations": {
                "required": required_status
            }
        },
        "Number": {
            "ref": ref,
            "title": title,
            "type": "number",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status,
                "min_value": 20,
                "max_value": 50
            }
        },
        "Opinion Scale": {
            "ref": ref,
            "title": title,
            "type": "opinion_scale",
            "properties": {
                    "description": description,
                    "steps": 9,
                    "start_at_one": True,
                    "labels": {
                    "left": "left label",
                    "center": "center label",
                    "right": "right label"
                }
            },
            "validations": {
                "required": required_status
            }
        },
        "Picture Choice": {
            "ref": ref,
            "title": title,
            "type": "picture_choice",
            "properties": {
                "description": description,
                "randomize": randomize,
                "allow_multiple_selection": allow_multiple_selection,
                "allow_other_choice": False,
                "supersized": False,
                "show_labels": False,
                "choices": choices_arr
            },
            "validations": {
                "required": required_status
            }
        },
        "Rating": {
            "ref": ref,
            "title": title,
            "type": "rating",
            "properties": {
                "description": description,
                "steps": 10,
                "shape": "star"
            },
            "validations": {
                "required": required_status
            }
        },
        "Short Text": {
            "ref": ref,
            "title": title,
            "type": "short_text",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status,
                "max_length": 20
            }
        },
        "Statement": {
            "ref": ref,
            "title": title,
            "type": "statement",
            "properties": {
                "description": description,
                "button_text": button_text,
                "hide_marks": True
            }
        },
        "Website": {
            "ref": ref,
            "title": title,
            "type": "website",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status
            }
        },
        "Yes/No": {
            "ref": ref,
            "title": title,
            "type": "yes_no",
            "properties": {
                "description": description
            },
            "validations": {
                "required": required_status
            }
        },
        "Group": {
            "ref": ref,
            "title": title,
            "type": "group",
            "properties": {
                "description": description,
                "show_button": True,
                "button_text": button_text,
                "fields": [
                    {
                        "ref": "nice_readable_website_reference_1",
                        "title": "website",
                        "type": "website",
                        "properties": {
                            "description": "Cool description for the website"
                        }
                    }
                ]
            }
        },
        "Matrix": {
            "ref": ref,
            "title": title,
            "type": "matrix",
            "properties": {
                "description": description,
                "fields": [
                    {
                        "ref": "nice_readable_multiple_choice_reference_inside_matrix",
                        "title": "multiple choice",
                        "type": "multiple_choice",
                        "properties": {
                            "description": "Cool description for the multiple choice in the matrix",
                            "allow_multiple_selection": allow_multiple_selection,
                            "allow_other_choice": False,
                            "vertical_alignment": True,
                            "choices": choices_arr
                        }
                    }
                ]
            }
        }
    }

    if (type_field in fields):
        return fields[type_field]

    return False

def getDataForForm():
    def getUtmStatus():
        arr_que_order = data_excel['arr_que_order']
        arr_utm = data_excel['arr_utm']
        for i in range(0, len(arr_que_order)):
            if (str(arr_que_order[i]) == str(item_logic)):
                return arr_utm[i]
        return False
    def setLogicItem(type):
        jump_to = f'element_{item_logic}'
        item = {}
        if type == 'end':
            item = {
                'type': 'field',
                'ref': ref,
                'actions': [
                    {
                        'action': 'jump',
                        'details': {
                            'to': {
                                'type': 'thankyou',
                                'value': 'end-win'
                                }
                            },
                        'condition': {
                            'op': 'always',
                            'vars': []
                        }
                    }
                ]
            }
        elif type == 'utm':
            item = {
                "type": "field",
                "ref": ref,
                "actions": [
                    {
                        "action": "jump",
                        "details": {
                            "to": {
                                "type": "field",
                                "value": jump_to
                            }
                        },
                        "condition": {
                            "op": "equal",
                            "vars": [
                                {
                                    "type": 'hidden',
                                    "value": "utm_campaign"
                                },
                                {
                                    "type": "constant",
                                    "value": str(utm)
                                }
                            ]
                        }
                    }
                ]
            }
        else:
            item = {
                'type': 'field',
                'ref': ref,
                'actions': [
                    {
                        'action': 'jump',
                        'details': {
                            'to': {
                                'type': 'field',
                                'value': jump_to
                                }
                            },
                        'condition': {
                            'op': 'always',
                            'vars': []
                        }
                    }
                ]
            }
        
        return item
               
    
    data_excel = getDataFromExcel()

    arr_fields = []
    arr_logic = []

    num_el = 1
    for i in range(0, len(data_excel['arr_que_order'])):
         # Настройки для каждого поля
        title = ""
        ref = ""
        description = ""
        required_status = True
        choices_arr = [] # ITEM: { 'label': 'Описание', 'ref': 'auto_gen_x' }
        allow_multiple_selection = False
        randomize = False

        num = data_excel['arr_que_order'][i]
        if num:
            type_field = data_excel['arr_que_type'][i]
            ref = f'element_{num_el}'
            title = data_excel['arr_data'][i][0]
            required_status = data_excel['arr_required'][i]
            allow_multiple_selection = data_excel['arr_multy_select'][i]
            randomize = data_excel['arr_random'][i]

            type_data = data_excel['arr_type_data'][i]

            row_logic = str(data_excel['arr_logic'][i]).split('.')
            for item_logic in row_logic:
                if (str(item_logic).lower() == 'end'):
                    arr_logic.append(setLogicItem('end'))
                else:
                    utm = getUtmStatus()
                    if str(utm).lower() == 'для всех' or not utm:
                        arr_logic.append(setLogicItem('jump'))
                    else:
                        arr_logic.append(setLogicItem('utm'))

            if (type_data == 'Вопрос'):
                if (len(data_excel['arr_data'][i+1]) > 1):
                    for x in range(0, len(data_excel['arr_data'][i+1])):
                        choices_arr.append({ 'label': data_excel['arr_data'][i+1][x], 'ref': f'element_{num_el}_{x}' })
                        required_status = data_excel['arr_required'][i+1]
                        allow_multiple_selection = data_excel['arr_multy_select'][i+1]
                        randomize = data_excel['arr_random'][i+1]

            field = setQuestionForParams(ref, title, description, required_status, choices_arr, allow_multiple_selection, randomize, type_field)
            if not field:
                return False

            arr_fields.append(field)

            num_el += 1

    return { "arr_fields": arr_fields, "form_name": data_excel['form_name'], 'arr_logic': arr_logic }

def setForm():
    try:
        id_workspace = getIdFirstWorkspace()
        url_workspace = f"https://api.typeform.com/workspaces/{id_workspace}"

        welcome_text = "Здравствуйте!Примите пожалуйста участие в нашем опросе ..."
        end_text = 'Спасибо за Участие!'

        data_form = getDataForForm()
        form_name = data_form['form_name']
        arr_fields = data_form['arr_fields']
        arr_logic = data_form['arr_logic']

        create_params = {
            "title": form_name,
            "type": "form",
            "settings": {
                "language": "ru",
                "is_public": False,
                "progress_bar": "percentage",
                "show_progress_bar": False,
                "show_typeform_branding": True,
                "show_time_to_complete": True,
                "hide_navigation": False
            },
            "workspace": {
                "href": url_workspace
            },
            "hidden": [
                "utm_source",
                "utm_campaign",
                "utm_content",
                "utm_term"
            ],
            "welcome_screens": [
                {
                    "ref": "welcome-win",
                    "title": welcome_text,
                    "properties": {
                        "description": "",
                        "show_button": True,
                        "button_text": "Начать"
                    },
                    "layout": {
                        "attachment": {
                            "type": "image",
                            "href": "https://images.typeform.com/images/4BKUhw8A9cSM"
                        },
                        "type": "split",
                        "placement": "left"
                    }
                }
            ],
            "thankyou_screens": [
                {
                    "ref": "end-win",
                    "title": end_text
                }
            ],
            "fields": arr_fields,
            'logic': arr_logic
        }

        r = req.post(f"{main_url}/forms", headers=headers, data=json.dumps(create_params))

        return r.status_code == req.codes.created

    except:
        return False