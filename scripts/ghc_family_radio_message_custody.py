#!/usr/bin/env python3
"""Run Caelen Ash v655-v6 bounded contract group 4: station startup and shutdown state, readback, abort, and physical-operation refusal, synthetic contact log, time, peer minimization, correction, retention, and contact-claim refusal, emergency-message custody, content minimization, relay, acknowledgement, and dispatch refusal."""

from ghc_family_v655_v6_core import group_main


if __name__ == "__main__":
    group_main(4, "ghc_family_radio_message_custody")
