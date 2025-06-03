import pandas as pd
from qiskit_ibm_provider import IBMProvider
from datetime import datetime, timedelta
import time

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(file_path)
    return df

def load_api_data(token, backend_name, limit=500):
    """
    Connect to IBM Quantum API and retrieve job metadata for a given backend.

    Parameters:
    token (str): IBM Quantum API token.
    backend_name (str): Name of the backend (e.g., 'ibm_sherbrooke').
    limit (int): Maximum number of jobs to retrieve.

    Returns:
    pd.DataFrame: DataFrame containing job metadata.
    """
    provider = IBMProvider(token=token)
    backend = provider.get_backend(backend_name)
    jobs = backend.jobs(limit=limit, retrieve=True)

    records = []
    for job in jobs:
        try:
            job_id = job.job_id()
            creation_date = job.creation_date()
            backend_name = job.backend().name
            result = job.result()

            for exp in result.results:
                try:
                    qubit_count = exp.header.get("n_qubits", None)
                    duration = exp.header.get("duration", None)
                    shots = exp.shots
                    success = exp.status.name if hasattr(exp, 'status') else None

                    records.append({
                        "job_id": job_id,
                        "creation_date": creation_date,
                        "backend": backend_name,
                        "qubit_count": qubit_count,
                        "duration": duration,
                        "shots": shots,
                        "success": success
                    })
                except Exception:
                    continue
        except Exception:
            continue

    df = pd.DataFrame(records)
    return df

def load_calibration_history(token, backend_name, start_date, end_date, step_days=1):
    """
    Retrieve calibration data (T1, T2, frequencies, errors) for a backend over time.

    Parameters:
    token (str): IBM Quantum API token.
    backend_name (str): Name of the backend (e.g., 'ibm_sherbrooke').
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    step_days (int): Interval in days between requests.

    Returns:
    pd.DataFrame: DataFrame with calibration parameters for each qubit and date.
    """
    provider = IBMProvider(token=token)
    backend = provider.get_backend(backend_name)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=step_days)

    records = []
    current = start
    while current <= end:
        try:
            properties = backend.properties(datetime=current)
            date_str = current.strftime("%Y-%m-%d")
            num_qubits = len(properties.qubits)

            # Initialize one record per qubit with calibration fields
            for i, qubit_props in enumerate(properties.qubits):
                record = {
                    "date": date_str,
                    "qubit": i,
                    "T1 (us)": qubit_props[1].value if len(qubit_props) > 1 else None,
                    "T2 (us)": qubit_props[2].value if len(qubit_props) > 2 else None,
                    "Frequency (GHz)": qubit_props[0].value if len(qubit_props) > 0 else None,
                    "Anharmonicity (GHz)": qubit_props[3].value if len(qubit_props) > 3 else None,
                    "Readout assignment error": qubit_props[4].value if len(qubit_props) > 4 else None,
                    "Prob meas0 prep1": qubit_props[5].value if len(qubit_props) > 5 else None,
                    "Prob meas1 prep0": qubit_props[6].value if len(qubit_props) > 6 else None,
                    "Readout length (ns)": qubit_props[7].value if len(qubit_props) > 7 else None,
                    "ID error": None,
                    "Z-axis rotation (rz) error": None,
                    "√x (sx) error": None,
                    "Pauli-X error": None,
                    "ECR error": None,
                    "Gate time (ns)": None,
                    "Operational": None
                }
                records.append(record)

            # Extract gate errors and lengths
            for gate in properties.gates:
                for param in gate.parameters:
                    if param.name == "gate_error":
                        for q in gate.qubits:
                            idx = (date_str, q)
                            records[q]["ID error"] = param.value if "id" in gate.name else records[q]["ID error"]
                            records[q]["Z-axis rotation (rz) error"] = param.value if "rz" in gate.name else records[q]["Z-axis rotation (rz) error"]
                            records[q]["√x (sx) error"] = param.value if "sx" in gate.name else records[q]["√x (sx) error"]
                            records[q]["Pauli-X error"] = param.value if "x" == gate.name else records[q]["Pauli-X error"]
                            records[q]["ECR error"] = param.value if "ecr" in gate.name else records[q]["ECR error"]
                    if param.name == "gate_length":
                        for q in gate.qubits:
                            records[q]["Gate time (ns)"] = param.value

            # Extract readout error and operational status
            for i, ro in enumerate(properties.readout_error):
                records[i]["Readout assignment error"] = ro.value
            for i, op in enumerate(properties.qubits):
                records[i]["Operational"] = 1  # Qubit exists => operational

        except Exception:
            pass

        current += delta
        time.sleep(1)

    df = pd.DataFrame(records)
    return df

def data_overview(df):
    """
    Display a general overview of a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame to inspect.

    This function prints:
    - First 5 rows (head)
    - Shape (rows, columns)
    - Column names
    - Data types
    - Missing values per column
    - Number of duplicated rows
    - DataFrame info (non-null counts)
    """
    print("DataFrame Head")
    print(df.head(), "\n")

    print("Shape")
    print(df.shape, "\n")

    print("Columns")
    print(df.columns.tolist(), "\n")

    print("Data Types")
    print(df.dtypes, "\n")

    print("Missing Values")
    print(df.isnull().sum(), "\n")

    print("Duplicated Rows")
    print(df.duplicated().sum(), "\n")

    print("DataFrame Info")
    print(df.info(), "\n")

def remove_duplicates(df):
    """
    Remove duplicated rows from a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame to process.

    Returns:
    pd.DataFrame: DataFrame without duplicate rows.
    """
    df_clean = df.drop_duplicates().reset_index(drop=True)
    return df_clean
