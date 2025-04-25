from controllers import RollingBasis, Actuators
from logger import Logger, LogLevels

logger_rolling_basis = Logger(
    identifier="rolling_basis",
    decorator_level=LogLevels.INFO,
    print_log_level=LogLevels.DEBUG,
    file_log_level=LogLevels.DEBUG,
)

rolling_basis = RollingBasis(logger=logger_rolling_basis)
rolling_basis.stop_and_clear_queue()
rolling_basis.set_pids(30.0, 0.0, 0.4, 30.0, 0.0, 0.4)
rolling_basis.set_odo(0, 0, 0)
rolling_basis.go_to(10, 0, 0)
