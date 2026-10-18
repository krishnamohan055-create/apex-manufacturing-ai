"""
Industrial Machine Telemetry Generator and Anomaly Simulator
Simulates real-time IoT sensor streams for industrial manufacturing equipment.
"""

import time
import random
import datetime
from typing import Dict, Any, List

MACHINES = {
    "CNC-4001": {
        "name": "5-Axis CNC Milling Center",
        "bay": "Bay 3 - Powertrain",
        "type": "Machining",
        "primary_metric": "Vibration (mm/s RMS)",
        "baseline": {
            "vibration": 1.4,
            "temperature": 42.0,
            "rpm": 8200,
            "spindle_load": 48.0,
            "coolant_flow": 12.5,
            "power_kw": 22.4,
            "oee": 91.2
        },
        "thresholds": {
            "vibration_warn": 3.0,
            "vibration_crit": 4.5,
            "temp_warn": 65.0,
            "temp_crit": 80.0,
            "load_warn": 75.0,
            "load_crit": 88.0
        }
    },
    "HYD-1020": {
        "name": "Heavy Hydraulic Stamping Press",
        "bay": "Bay 1 - Body Stamping",
        "type": "Hydraulics",
        "primary_metric": "System Pressure (bar)",
        "baseline": {
            "pressure": 210.0,
            "temperature": 52.0,
            "vibration": 0.9,
            "cycle_time": 4.2,
            "oil_viscosity": 46.0,
            "power_kw": 45.0,
            "oee": 88.5
        },
        "thresholds": {
            "pressure_low_warn": 180.0,
            "pressure_low_crit": 140.0,
            "temp_warn": 70.0,
            "temp_crit": 85.0,
            "cycle_warn": 5.5,
            "cycle_crit": 7.0
        }
    },
    "INJ-880": {
        "name": "Polymer Injection Molding Cell",
        "bay": "Bay 4 - Interior Trim",
        "type": "Molding",
        "primary_metric": "Barrel Temp (°C)",
        "baseline": {
            "barrel_temp": 220.0,
            "injection_pressure": 145.0,
            "clamp_force": 880.0,
            "cooling_time": 12.0,
            "vibration": 0.5,
            "power_kw": 34.2,
            "oee": 94.0
        },
        "thresholds": {
            "barrel_temp_warn": 235.0,
            "barrel_temp_crit": 248.0,
            "inj_pressure_warn": 165.0,
            "inj_pressure_crit": 180.0
        }
    },
    "ROB-W05": {
        "name": "6-Axis Robotic Seam Welder",
        "bay": "Bay 2 - Chassis Assembly",
        "type": "Robotics",
        "primary_metric": "Tip Temperature (°C)",
        "baseline": {
            "arc_current": 162.0,
            "gas_flow": 15.2,
            "tip_temp": 315.0,
            "joint_vibration": 0.6,
            "feed_speed": 450.0,
            "power_kw": 18.5,
            "oee": 89.8
        },
        "thresholds": {
            "tip_temp_warn": 360.0,
            "tip_temp_crit": 410.0,
            "gas_flow_low_warn": 12.0,
            "gas_flow_low_crit": 9.0
        }
    }
}

ANOMALY_TYPES = {
    "BEARING_DEGRADATION": {
        "target_machine": "CNC-4001",
        "label": "Spindle Bearing Raceway Pitting & Spalling",
        "description": "Inner raceway micro-fracture causing high frequency vibration harmonic spikes and rapid frictional heating.",
        "effects": {
            "vibration": 5.85,
            "temperature": 78.4,
            "spindle_load": 74.0,
            "power_kw": 31.8,
            "oee": 62.4
        }
    },
    "HYDRAULIC_CAVITATION": {
        "target_machine": "HYD-1020",
        "label": "Hydraulic Proportional Valve Cavitation & Pressure Drop",
        "description": "Air ingress and oil aeration in main hydraulic manifold causing cylinder pressure loss and sluggish cycle times.",
        "effects": {
            "pressure": 124.0,
            "temperature": 79.2,
            "cycle_time": 7.4,
            "vibration": 2.8,
            "oee": 54.1
        }
    },
    "THERMAL_RUNAWAY": {
        "target_machine": "INJ-880",
        "label": "Molding Barrel Thermal Runaway & Nozzle Blockage",
        "description": "Thermocouple feedback drift causing PID heater loop saturation, resulting in resin degradation and nozzle backpressure.",
        "effects": {
            "barrel_temp": 252.0,
            "injection_pressure": 178.5,
            "vibration": 1.2,
            "oee": 48.0
        }
    },
    "SHIELD_GAS_DEFECT": {
        "target_machine": "ROB-W05",
        "label": "Shielding Gas Line Obstruction & Arc Instability",
        "description": "Argon gas solenoid throttling creating severe weld porosity risk and excessive contact tip thermal dissipation.",
        "effects": {
            "gas_flow": 7.8,
            "tip_temp": 425.0,
            "arc_current": 188.0,
            "oee": 51.5
        }
    }
}

def generate_telemetry_snapshot(machine_id: str, active_anomaly: str = None) -> Dict[str, Any]:
    """Generates a single telemetry snapshot with realistic jitter or anomaly injection."""
    config = MACHINES.get(machine_id, MACHINES["CNC-4001"])
    baseline = dict(config["baseline"])
    
    # Apply baseline jitter (+/- 2% random variation)
    snapshot = {}
    for key, val in baseline.items():
        jitter = val * (1.0 + random.uniform(-0.025, 0.025))
        snapshot[key] = round(jitter, 2)
        
    status = "HEALTHY"
    anomaly_desc = None
    
    # Inject anomaly if active on this machine
    if active_anomaly and active_anomaly in ANOMALY_TYPES:
        anomaly_cfg = ANOMALY_TYPES[active_anomaly]
        if anomaly_cfg["target_machine"] == machine_id:
            for key, val in anomaly_cfg["effects"].items():
                jitter = val * (1.0 + random.uniform(-0.015, 0.015))
                snapshot[key] = round(jitter, 2)
            status = "CRITICAL_ANOMALY"
            anomaly_desc = anomaly_cfg["description"]

    return {
        "machine_id": machine_id,
        "machine_name": config["name"],
        "bay": config["bay"],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "anomaly_code": active_anomaly if status == "CRITICAL_ANOMALY" else None,
        "anomaly_description": anomaly_desc,
        "metrics": snapshot,
        "thresholds": config["thresholds"]
    }

def generate_historical_series(machine_id: str, points: int = 25, active_anomaly: str = None) -> List[Dict[str, Any]]:
    """Generates a time-series history for charts with recent anomaly ramp-up if active."""
    history = []
    base_time = datetime.datetime.now() - datetime.timedelta(minutes=points)
    
    for i in range(points):
        t = base_time + datetime.timedelta(minutes=i)
        # If anomaly is active, simulate ramping up in the last 6 points
        is_anomaly_point = (active_anomaly is not None) and (i >= points - 6)
        curr_anomaly = active_anomaly if is_anomaly_point else None
        
        snap = generate_telemetry_snapshot(machine_id, curr_anomaly)
        snap["timestamp"] = t.strftime("%H:%M:%S")
        history.append(snap)
        
    return history
