json_to_validate = {
    'string': 'sample_string',
    'float': 1.0,
    'integer': 1,
    'bool': False,
    'list': [1, 2, 3, 4],
    'dictionary': {
        'string': 'sample_string',
        'list': [1, 2, 3, 4],
        'dictionary': {
            'array': [{'string': 'a'}, {'string': 'b'}, {'string': 'c'}],
        }
    }
}

schema_this_json_represents = {
    'string': {
        'required': False,
        'type': str
    },
    'float': {
        'required': True,
        'type': float
    },
    'integer': {
        'required': True,
        'type': int
    },
    'bool': {
        'required': True,
        'type': bool
    },
    'list': {
        'required': True,
        'type': list,
        'schema': {
            'required': True,
            'type': int
        }
    },
    'dictionary': {
        'required': True,
        'type': dict,
        'schema': {
            'string': {
                'required': True,
                'type': str
            },
            'list': {
                'required': True,
                'type': list,
                'schema': {
                    'required': True,
                    'type': int
                }
            },
            'dictionary': {
                'type': dict,
                'required': True,
                'schema': {
                    'type': list,
                    'required': True,
                    'schema': {
                        'type': 'dictionary',
                        'schema': {
                            'type': str
                        }
                    }
                }
            }
        }
    }
}


def get_name(item):
    return item[0]


def get_content(item):
    return item[1]


def have_proper_naming(key_name, validation_name):
    return key_name == validation_name


def have_proper_type(key_content, validation_content):
    return isinstance(key_content, validation_content.get('type'))


def required_key(validation_content):
    return validation_content.get('required')


def validate_key(key, validation):
    key_name = get_name(key)
    validation_name = get_name(validation)

    key_content = get_content(key)
    validation_content = get_content(validation)

    # Ideally i want to apply functions from array to each (key, validation) pair (as if it is map but not exactly)
    # like (pair) <= [function1, function2, ... functionN]
    # having this validation process implemented we will be just writing new validation functions

    # for this example lets hardcode some "if"s.
    required = required_key(validation_content)
    # possible to play with required condition but just bare with me, that
    # in this examples not required are not validated for simplicity
    if required:
        if have_proper_naming(key_name, validation_name):
            have_proper_type(key_content, validation_content)
            print('valid_key')


def validate_against_schema(json, schema):
    json_representation = json.items()
    schema_representation = schema.items()

    structured = list(zip(json_representation, schema_representation))
    for item in structured:
        entry = item[0]
        schema = item[1]
        print(entry, schema)
        validate_key(entry, schema)


print("VALIDATING AGAINST SCHEMA")
validate_against_schema(json_to_validate, schema_this_json_represents)
print('')
print('')

sample_changeable_schema = {
    'string': {
        'type': str,
        'required': True
    },
    'dictionary': {
        'type': dict,
        'schema': {
            'type': dict,
            'required': True,
            'schema': {
                'type': dict,
                'required': False
            }
        }
    }
}


# Example how to change schema
def change_required_values(schema, list_of_values, change_to):
    """ Take <schema> and for each key from <list_of_values> change required <change_to>"""
    for value in list_of_values:
        schema_entry = schema.get(value)
        schema_entry.update({'required': change_to})

    return schema


updated = change_required_values(sample_changeable_schema, ['string'], False)

print("UPDATING SCHEMA")
print(updated)

# So in a way we can have one schema, describing some yamls batch (like for questionnaire), then
# Validate as in validate_against_schema and change schema with different functions, e.g. change_required_values.
# Again if multiple changes are necessary: just (schema) <= [changing_function1, changing_function2, ..., etc]
# Limitations: 1). we should know what yaml must be what and adjust schemas for it
#              2). will be hard to reference nested keys and values but only in the beginning
# Benefits: 1). one schema (for yaml batch) which we can both manually and programmatically change.
#           2). No rewriting of functions which are used during the validation (e.g. have_proper_naming, small ones)
#           3). Very flexible structure of applying functions during the validation ((pair) <= [f1, f2, ...]). Allows
#               to do anything
