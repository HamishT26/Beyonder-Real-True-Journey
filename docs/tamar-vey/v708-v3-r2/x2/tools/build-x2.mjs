import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  buildNexusEnvelope,
  compareEnvironment,
  evaluatePrivilege,
  reconcileSetup,
  reduceRouteEvidence,
  verifySourceBinding,
} from "./nexus-x2-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const x2 = path.resolve(here, "..");
const read = (relative) =>
  JSON.parse(fs.readFileSync(path.join(x2, relative), "utf8"));
const write = (relative, value) => {
  const target = path.join(x2, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
};

const binding = read("fixtures/source-binding.json");
const environment = read("fixtures/environment-drift.json");
const route = read("fixtures/route-evidence.json");
const setup = read("fixtures/partial-setup.json");

const source = verifySourceBinding(binding);
const drift = compareEnvironment(environment.requested, environment.observed);
const routeState = reduceRouteEvidence(route.events);
const reconciliation = reconcileSetup(setup.prior, setup.plan);
const privilege = {
  inspect_repository: evaluatePrivilege("inspect_repository", {
    observed_grants: ["workspace_read"],
  }),
  write_owner_repository: evaluatePrivilege("write_owner_repository", {
    observed_grants: ["workspace_write", "owner_scope"],
  }),
  publish_cloud_environment: evaluatePrivilege("publish_cloud_environment", {
    observed_grants: ["cloud_publish"],
  }),
  mutate_host_security: evaluatePrivilege("mutate_host_security", {
    observed_grants: ["full_access_label"],
  }),
};

write("evidence/source-binding-result.json", source);
write("evidence/environment-drift-report.json", drift);
write("evidence/privilege-action-report.json", privilege);
write("evidence/route-state-report.json", routeState);
write("evidence/setup-reconciliation-report.json", reconciliation);
write(
  "evidence/nexus-envelope.json",
  buildNexusEnvelope({
    source,
    payload: binding.payload,
    environment: drift,
    route: routeState,
    reconciliation,
  }),
);

write("build-receipt.json", {
  schema: "ghc.tamar.v708-v3-r2.x2-build-receipt.v1",
  status: "BUILT_NOT_VALIDATED",
  source_binding_ok: source.ok,
  environment_exact_match: drift.exact_match,
  route_acknowledged: routeState.acknowledged,
  route_recipient_completed: routeState.recipient_completed,
  completed_setup_steps: reconciliation.completed.length,
  retained_setup_failures: reconciliation.failures.length,
  cloud_publication_allowed: privilege.publish_cloud_environment.allowed,
  host_security_mutation_allowed: privilege.mutate_host_security.allowed,
});
