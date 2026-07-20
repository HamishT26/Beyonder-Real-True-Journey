#!/usr/bin/env python3
"""Mutable-until-seal v650-v6 closeout operational-negative input."""

CLOSEOUT_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6506-CLOSE-N01",
        "category": "closeout test privacy-token hit",
        "failed": "The first closeout build found two literal prohibited scanner tokens inside test assertions and refused to seal.",
        "recovery": "Retain the failed scan with zero privacy credit and construct the forbidden test strings from harmless fragments so artifacts still verify absence without carrying literal payload tokens.",
        "passing": "The rebuilt closeout tree passes all five structural scan classes with zero confirmed payload hits.",
        "recurrence_guard": "Quarantine scanner definitions and construct negative-test needles without embedding prohibited literal payload tokens.",
    },
]
