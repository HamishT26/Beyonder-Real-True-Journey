/**
 * Validate one bounded synthetic letterpress status object.
 * @param {{ syntheticOnly?: boolean, authoritative?: boolean, terminalVerdict?: string } | null | undefined} value
 */
export function validateStatus(value) {
  return Boolean(
    value &&
    value.syntheticOnly === true &&
    value.authoritative === false &&
    value.terminalVerdict === "NOT_READY_FOR_STAGE_20",
  );
}

const smoke = {
  syntheticOnly: true,
  authoritative: false,
  terminalVerdict: "NOT_READY_FOR_STAGE_20",
};
console.log(JSON.stringify({ passed: validateStatus(smoke) }));
