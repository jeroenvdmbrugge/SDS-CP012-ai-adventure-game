import os
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print(os.environ)
print('home' in os.environ) # True of False
#print('OPENAI_API_KEY' in os.environ) # True of False
#print(os.environ['OPENAI_API_KEY']) # Print contents of variable
#print(os.environ.get('OPENAI_API_KEY')) # Its better when variable not existed

BOOLEAN_TYPE = 'boolean'
INT_TYPE = 'int'
FLOAT_TYPE = 'float'
STRING_TYPE = 'str'
LIST_TYPE = 'list'
DICT_TYPE = 'dict'


def get_envvars(env_file='.env', set_environ=True, ignore_not_found_error=False, exclude_override=()):
    """
    Set env vars from a file
    :param env_file:
    :param set_environ:
    :param ignore_not_found_error: ignore not found error
    :param exclude_override: if parameter found in this list, don't overwrite environment
    :return: list of tuples, env vars
    """
    env_vars = []
    try:

        with open(env_file) as f:
            for line in f:
                line = line.replace('\n', '')

                if not line or line.startswith('#'):
                    continue

                # Remove leading `export `
                if line.lower().startswith('export '):
                    key, value = line.replace('export ', '', 1).strip().split('=', 1)
                else:
                    try:
                        key, value = line.strip().split('=', 1)
                    except ValueError:
                        logging.error(f"envar_utils.get_envvars error parsing line: '{line}'")
                        raise

                if set_environ and key not in exclude_override:
                    os.environ[key] = value

                if key in exclude_override:
                    env_vars.append({'name': key, 'value': os.getenv(key)})
                else:
                    env_vars.append({'name': key, 'value': value})
    except FileNotFoundError:
        if not ignore_not_found_error:
            raise
        print(env_vars)

    return env_vars


def create_envvar_file(env_file_path, envvars):
    """
    Writes envvar file using env var dict
    :param env_file_path: str, path to file to write to
    :param envvars: dict, env vars
    :return:
    """
    with open(env_file_path, "w+") as f:
        for key, value in envvars.items():
            f.write("{}={}\n".format(key, value))
    return True


def convert_env_var_flag_to(env_var_name, required_type, default_value):
    """
    Convert env variable string flag values to required_type
    :param env_var_name: str, environment variable name
    :param required_type: str, required type to cast the env var to
    :param default_value: boolean, default value to use if the environment variable is not available
    :return: environment variable value in required type
    """
    env_var_orginal_value = os.getenv(env_var_name, default_value)
    env_var_value = ""
    try:
        if required_type == INT_TYPE:
            env_var_value = int(env_var_orginal_value)
        elif required_type == FLOAT_TYPE:
            env_var_value = float(env_var_orginal_value)
        elif required_type == BOOLEAN_TYPE:
            env_var_value = bool(int(env_var_orginal_value))
        elif required_type == STRING_TYPE:
            env_var_value = str(env_var_orginal_value)
        elif required_type == LIST_TYPE:
            env_var_value = env_var_orginal_value.split(',') if len(env_var_orginal_value) > 0 else default_value
        elif required_type == DICT_TYPE:
            try:
                env_var_value = json.loads(env_var_orginal_value) if env_var_orginal_value else default_value
            except Exception as e:
                logging.error(f"convert_env_var_flag_to: failed loading {env_var_orginal_value} error {e}")
                env_var_value = default_value
        else:
            logging.error("Unrecognized type {} for env var {}".format(required_type, env_var_name))

    except ValueError:
        env_var_value = default_value
        logging.warning("{} is {}".format(env_var_name, env_var_orginal_value))

    return env_var_value


mykey = os.getenv('OPENAI_API_KEY')
print (mykey)
client = OpenAI(mykey)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a dungeon master and you will create a text based fantasy adventure game for a user to play and interact with using text. Generate a fantasy land and story for a short text based adventure game and describe it to the user. Ask them to pick between 3 different avatars: Wizard, archer, swordsman. For each avatar, give the user a short description of the abilities of each, health points, and the moves each one of them has."},
        {
            "role": "user",
            "content": "What is the game and what are the game rules?"
        }
    ]
)

print(completion.choices[0].message)