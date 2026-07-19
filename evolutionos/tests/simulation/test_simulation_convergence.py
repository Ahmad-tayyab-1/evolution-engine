"""
Simulation Convergence Verification Gate (`SIM-001`, `FR-EC-601`).

Verifies that:
1. `SimulationRunner` discovers `>= 80%` of planted ground-truth rules within `<= 50` cycles.
2. Calibration error is bounded within `±15%` (`max_calibration_error = 0.15`).
3. Immutability invariants hold across the run (`zero_mutated_records = True`).
"""
import pytest
from evolutionos.simulation.world import SyntheticWorld
from evolutionos.simulation.runner import SimulationRunner
from evolutionos.config.settings import settings


def test_sim_001_simulation_convergence_gate():
    """SIM-001 verification gate: require >= 80% discovery of planted rules in <= 50 cycles."""
    world = SyntheticWorld()
    runner = SimulationRunner(world=world)

    results = runner.run_simulation(max_cycles=settings.sim_max_cycles)

    # Assert discovery rate >= min_discovery_rate (default 0.80 -> 80%)
    assert results["discovery_rate"] >= settings.sim_min_discovery_rate, (
        f"SIM-001 Failure: Discovered only {results['discovery_rate']*100:.1f}% of planted rules "
        f"({results['discovered_rules_count']}/{results['total_planted_rules']}), required >= {settings.sim_min_discovery_rate*100:.1f}%."
    )

    # Assert cycle budget respected (<= 50 cycles)
    assert results["cycles_run"] <= settings.sim_max_cycles, (
        f"SIM-001 Failure: Ran {results['cycles_run']} cycles, max allowed is {settings.sim_max_cycles}."
    )

    # Assert calibration error bounded (within +-15%)
    assert results["calibration_error"] <= settings.sim_max_calibration_error, (
        f"SIM-001 Failure: Calibration error {results['calibration_error']} exceeds threshold {settings.sim_max_calibration_error}."
    )

    # Assert immutability
    assert results["zero_mutated_records"] is True
