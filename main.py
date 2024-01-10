# Import necessary libraries
import json
import jinja2
import os
import shutil
import yaml

from grafana_client import GrafanaApi

# Define script directory and file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
template_providers_path = os.path.join(script_dir, "template_providers.yml")
output_dir = os.path.join(script_dir, "output")
config_file = os.path.join(script_dir, "config.yaml")


def read_yaml_config():
    try:
        # Try to open the YAML configuration file for reading
        with open(config_file, "r") as file:
            # Load the YAML data from the file
            config_data = yaml.safe_load(file)
        # Return the loaded configuration data if successful
        return config_data
    except FileNotFoundError:
        # Handle the case when the file is not found
        print(f"File not found: {config_file}")
        return None
    except Exception as e:
        # Handle any other exceptions that might occur during reading
        print(f"Error reading YAML config file: {str(e)}")
        return None


# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_name):
    try:
        # Create the full path to the folder
        folder_path = os.path.join(output_dir, folder_name)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created at: {folder_path}")
        else:
            print(f"Folder '{folder_name}' already exists at: {folder_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Function to clear and recreate the output directory
def flush_output_dir():
    try:
        # Check if the directory exists
        if os.path.exists(output_dir):
            # Delete the directory and its contents
            shutil.rmtree(output_dir)
            print(f"Directory '{output_dir}' deleted successfully.")
        else:
            print(f"Directory '{output_dir}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    create_folder_if_not_exists(output_dir)


# Function to write data to a file
def write_to_file(data, file_path, type=None):
    try:
        # Write the data to the file
        with open(file_path, "w") as output_file:
            if type == "json":
                print(type)
                json.dump(data, output_file, indent=4)
            else:
                output_file.write(data)

        print(f"Data written to: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Function to render a YAML template using Jinja2
def render_yaml_template(file_path, context):
    try:
        # Load the Jinja2 template
        template_loader = jinja2.FileSystemLoader(
            searchpath=os.path.dirname(template_providers_path)
        )
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(os.path.basename(template_providers_path))

        # Render the template with the provided context
        rendered_yaml = template.render(context)

        # Call the function to write the rendered data to a file
        write_to_file(rendered_yaml, file_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Main execution
if __name__ == "__main__":
    # Clear and recreate the output directory
    flush_output_dir()

    config = read_yaml_config()

    # Initialize Grafana API client
    grafana = GrafanaApi.from_url(
        url=config["grafanaURL"],
    )

    # Print a message indicating the start of dashboard processing
    print("List of dashboards")

    # Fetch a list of dashboards from Grafana
    dashboards = grafana.search.search_dashboards()

    # Print the list of dashboards in a human-readable format
    print(json.dumps(dashboards, indent=2))

    # Loop through each dashboard in the list
    for dashboard in dashboards:
        # Check if the dashboard type is not a folder (individual dashboard)
        if dashboard["type"] != "dash-folder":
            # Check if the dashboard has a "folderTitle" property
            if "folderTitle" in dashboard:
                # Extract the dashboard title and remove spaces for use in directory names
                dashboard_folder_name = dashboard["folderTitle"]
                dashboard_folder_name_merged = dashboard_folder_name.replace(" ", "")

                # Create a folder if it doesn't exist, using the modified dashboard title as the folder name
                create_folder_if_not_exists(dashboard_folder_name_merged)

                # Fetch the JSON data for the dashboard
                dashboard_data = grafana.dashboard.get_dashboard(
                    dashboard_uid=dashboard["uid"]
                )

                # Define the file paths for the dashboard JSON file and the provisioner YAML file
                dashboard_file_path = os.path.join(
                    output_dir,
                    dashboard_folder_name_merged,
                    (dashboard["uri"].replace("db/", "") + ".json"),
                )
                provisioner_file_path = os.path.join(
                    output_dir,
                    (dashboard_folder_name_merged + ".yaml"),
                )

                # Write the dashboard JSON data to a file
                write_to_file(dashboard_data["dashboard"], dashboard_file_path, "json")

                # Define a context dictionary with values to replace in the provisioner YAML template
                context = {
                    "name": dashboard_folder_name,
                    "folder": dashboard_folder_name,
                    "path": "/etc/grafana/provisioning/dashboards"
                    + "/"
                    + dashboard_folder_name_merged,
                }

                # Call the function to render the provisioner YAML template
                render_yaml_template(provisioner_file_path, context)
