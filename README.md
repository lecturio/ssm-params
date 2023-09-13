# ssm-params

CRUD AWS SSM Parameter Store operations for a project.

# Operations

- list -- lists the whole store for the files in the project root
- put -- sets new values remotely
- apply -- replaces placeholders in configuration files with remote values

# TODOS:

- add mode to specify value for empty remote param on the fly when applying
- add diff and clean
- prettify listing
