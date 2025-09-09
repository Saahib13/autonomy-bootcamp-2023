"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        self.has_landed = False
        # Add your own
        self.target_pad = None
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # Calculate distance to waypoint
        pos = report.position  # drone current position

        if self.has_landed:
            return command  # Already done

        # Helper logic inline: squared distance (avoid sqrt)
        def dist2(a: location.Location, b: location.Location) -> float:
            dx = a.location_x - b.location_x
            dy = a.location_y - b.location_y
            return dx * dx + dy * dy

        # If we haven't picked a pad yet, go to waypoint first
        if self.target_pad is None:
            if dist2(pos, self.waypoint) > self.acceptance_radius**2:
                # Still need to fly to waypoint
                if report.status.name == "HALTED":
                    dx = self.waypoint.location_x - pos.location_x
                    dy = self.waypoint.location_y - pos.location_y
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
            else:
                # Reached waypoint: choose closest landing pad
                if landing_pad_locations:
                    closest = None
                    min_dist = float("inf")
                    for pad in landing_pad_locations:
                        d = dist2(pos, pad)
                        if d < min_dist:
                            min_dist = d
                            closest = pad
                    self.target_pad = closest
                    print(f"Target pad selected: {self.target_pad}")
                else:
                    # No pads found, just land here
                    if report.status.name == "HALTED":
                        self.has_landed = True
                        command = commands.Command.create_land_command()
            return command

        # Now fly to the chosen landing pad
        if dist2(pos, self.target_pad) > self.acceptance_radius**2:
            if report.status.name == "HALTED":
                dx = self.target_pad.location_x - pos.location_x
                dy = self.target_pad.location_y - pos.location_y
                command = commands.Command.create_set_relative_destination_command(dx, dy)
        else:
            if report.status.name == "HALTED":
                self.has_landed = True
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
