# MathHammer10th

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your machine.
- Pip: Python's package installer.

## Setting Up Your Environment

To run this script, you should set up a virtual environment. This will keep your dependencies organized and your project isolated from the rest of your system. Here's how you can do it:

1. **Creating a Virtual Environment:**
    - Navigate to your project's directory in the terminal.
    - Run the command to create a virtual environment:
      ```bash
      python -m venv venv
      ```
    - This will create a directory called `venv` in your project folder.

2. **Activating the Virtual Environment:**
    - Activate the virtual environment by running:
      - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
      - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    - Your prompt will change to show the name of the activated environment.

## Installing Dependencies

With your virtual environment activated, install the required Python package:

- **SciPy:**
  - Install SciPy, which includes the `binom` function from the `scipy.stats` module, by running:
    ```bash
    pip install scipy
    ```

## Running the Script

- Ensure your virtual environment is active whenever you're working on the project.
- Run the script using:
  ```bash
  python path/to/your_script.py
  ```

## Deactivating the Virtual Environment

```bash
    deactivate
```
