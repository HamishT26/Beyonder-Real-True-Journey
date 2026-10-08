/** Owner-only presentation candidate. No I/O, sends, claims or admission decisions. */
import { renderFrame } from './terminal-presentation.mjs';

const nonempty = value => typeof value === 'string' && value.length > 0;
const validHost = target => target?.kind === 'chatgpt' ? target.hostId === null : nonempty(target?.hostId);
function bound(record, message) {
  return record && ['requestId', 'messageSha256'].every(key =>
    nonempty(message[key]) && record[key] === message[key]) &&
    nonempty(message.target?.threadId) && record.threadId === message.target.threadId &&
    validHost(message.target) && record.hostId === message.target.hostId;
}

function label(message) {
  if (message.schema !== 'ghc.nexus.message-status.v1' ||
      message.recipientCompletion !== 'not_observed') return 'UNKNOWN - summary not verified.';
  const claim = message.claim;
  const receipt = message.receipt;
  const claimMatches = claim?.schema === 'ghc.nexus.message-claim.v1' && bound(claim, message);
  const receiptMatches = claimMatches &&
    receipt?.schema === 'ghc.nexus.message-receipt.v1' && bound(receipt, message) &&
    receipt.evidenceType === 'caller-reported-native-tool-result' &&
    receipt.tool === 'mcp__codex_app__send_message_to_thread' &&
    receipt.recipientCompletion === 'not_observed' &&
    receipt.outcome === message.deliveryState;
  if (receiptMatches) {
    if (receipt.outcome === 'accepted') return 'ACKNOWLEDGED (caller-reported).';
    if (receipt.outcome === 'rejected') return 'REJECTED (caller-reported).';
    if (receipt.outcome === 'unknown') return 'UNKNOWN - caller reported an unknown outcome.';
  }
  if (message.deliveryState === 'queued' && !claim && !receipt) return 'QUEUED - not sent.';
  if (message.deliveryState === 'claimed_outcome_unknown' && claimMatches && !receipt)
    return 'UNKNOWN - claim recorded; reconcile the outcome.';
  return 'UNKNOWN - missing or conflicting evidence.';
}

/** Accept only the existing listMessages summary; keep its machine JSON API unchanged. */
export function renderDeliveryPanel(collection = {}, options = {}) {
  const messages = Array.isArray(collection?.messages) ? collection.messages : [];
  const lines = ['Delivery observations. Caller reports are not provider attestations.'];
  if (!messages.length) lines.push('No message records to display.');
  messages.slice(0, 100).forEach((value, index) => {
    const message = value && typeof value === 'object' ? value : {};
    lines.push('', `${index + 1}. Request: ${nonempty(message.requestId) ? message.requestId : 'unknown'}`,
      `Target ID: ${nonempty(message.target?.threadId) ? message.target.threadId : 'unknown'}`,
      `Host: ${message.target?.kind === 'chatgpt' && message.target.hostId === null ? 'ChatGPT provider' : nonempty(message.target?.hostId) ? message.target.hostId : 'unknown'}`,
      `Delivery: ${label(message)}`,
      'Recipient completion: NOT OBSERVED by this view.');
  });
  if (messages.length > 100) lines.push(`${messages.length - 100} records omitted; narrow the selection.`);
  return renderFrame({title:'DELIVERY OBSERVATIONS',lines,
    footer:['Display only; no send, resend, claim or resume permission is inferred.']}, options);
}
