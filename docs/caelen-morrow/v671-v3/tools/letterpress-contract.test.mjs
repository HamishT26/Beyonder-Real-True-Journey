import { describe, expect, test } from "vitest";
import { validateStatus } from "./letterpress-contract.mjs";

describe("bounded letterpress status", () => {
  test("accepts bounded synthetic state", () => {
    expect(
      validateStatus({
        syntheticOnly: true,
        authoritative: false,
        terminalVerdict: "NOT_READY_FOR_STAGE_20",
      }),
    ).toBe(true);
  });
  test("rejects authority promotion", () => {
    expect(
      validateStatus({
        syntheticOnly: true,
        authoritative: true,
        terminalVerdict: "NOT_READY_FOR_STAGE_20",
      }),
    ).toBe(false);
  });
});
