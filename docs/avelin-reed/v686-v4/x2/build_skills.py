"""Initialize, validate, smoke-use, then additively promote ten exact skills."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as output:
        output.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', required=True, type=Path)
    parser.add_argument('--validator-python', required=True, type=Path)
    parser.add_argument('--skill-root', required=True, type=Path)
    parser.add_argument('--creator-root', required=True, type=Path)
    args = parser.parse_args()
    plan = json.loads((ROOT / 'x1/skill-runner-plan.json').read_text(encoding='utf-8'))
    proposals = json.loads((ROOT / 'x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']
    runtime = json.loads((ROOT / 'x1/package-plan.json').read_text(encoding='utf-8'))
    runner_paths = sorted((ROOT / 'runners').glob('ghc_family_temporal_*.py'))
    assert len(runner_paths) == 5
    for skill in plan['skills']:
        if (ROOT / 'skills' / skill['name']).exists() or (args.skill_root / skill['name']).exists():
            raise RuntimeError('A planned skill destination already exists: ' + skill['name'])
    receipts = []
    local_reviews = []
    for skill in plan['skills']:
        name = skill['name']
        package = ROOT / 'skills' / name
        init = subprocess.run([str(args.validator_python), '-X', 'utf8', str(args.creator_root / 'scripts/init_skill.py'), name,
                               '--path', str(ROOT / 'skills'), '--resources', 'scripts,references',
                               '--interface', 'short_description=Inspect bounded temporal contract fixtures'], capture_output=True, text=True, encoding='utf-8')
        if init.returncode:
            raise RuntimeError('Skill initializer rejected ' + name + ': ' + init.stderr)
        selected = [p for p in proposals if p['family'] in skill['families']]
        runner = 'ghc_family_temporal_' + selected[0]['runner'] + '.py'
        families = ', '.join('`' + family + '`' for family in skill['families'])
        description = 'Inspect ' + ', '.join(family.replace('_', ' ') for family in skill['families']) + ' using bounded synthetic JSON fixtures and explicit evidence limits.'
        guide = f'''---
name: {name}
description: {json.dumps(description)}
---

# {name.removeprefix('ghc-family-').replace('-', ' ').title()}

Use this package for {families}. It combines two related frozen contract families from Avelin Reed v686-v4. A fixture is a bounded software example, and each input and expected result remains in [the contract reference](references/contracts.json).

Select the matching family by its actual operation and endpoint or record semantics. Do not substitute a similarly named family. Use the already authorized isolated runtime described in [runtime requirements](references/runtime.json). Merely finding this package does not authorize an installation or an external action.

Pass one JSON object containing exactly `family` and `input` to `python -X utf8 scripts/{runner} --input case.json --output result.json`. The output path must be new. The CLI emits stable refusal values for malformed inputs, so read the result JSON rather than treating exit code zero as acceptance of the proposed operation.

Compare the entire result, including JSON types, endpoint closures, record order, and refusal labels. Keep the original input unchanged. Use exact integer synthetic ticks; these examples provide no conversion between physical clocks. Retain every rejected input and use a new output path for its bounded correction.

The five portable runner sources are included so local imports remain available after relocation. Their copies are compatibility assets, not additional runner novelty. The original source and x1 definition digests in the reference identify the evidence contract; a copied guide does not transfer owner execution credit.

All names, roles, hopes, and family terms are relational working language only. A simulated allow result is not real authorization. Preserve empirical, participant, professional, production, identity, legal, cultural, affected-party, Māori-authority, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything, canon, and Stage 20 boundaries. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct.

Rollback by selecting the prior validated package. Preserve this package, its source, and every negative; do not overwrite another skill or repair an evidence mismatch by weakening a gate.
'''
        (package / 'SKILL.md').write_text(guide, encoding='utf-8', newline='\n')
        write(package / 'references/contracts.json', {'schema': 'ghc.family.temporal-skill-contracts.v1', 'owner': 'Avelin Reed', 'phase': 'v686-v4', 'source': 'c5cdc995c99bca100f5a63a4f3f23e932d9433a5', 'x1': '5fbfddafacbfdae773777a7e7591b473797491a5', 'families': skill['families'], 'proposals': selected})
        write(package / 'references/runtime.json', {'python': 'CPython 3.12', 'packages': [{'name': row['name'], 'version': row['version']} for row in runtime['packages']], 'installation_authority': False, 'synthetic_only': True})
        for source in runner_paths:
            shutil.copyfile(source, package / 'scripts' / source.name)
        validate = subprocess.run([str(args.validator_python), '-X', 'utf8', str(args.creator_root / 'scripts/quick_validate.py'), str(package)], capture_output=True, text=True, encoding='utf-8')
        local_reviews.append({'skill': name, 'validator_exit_code': validate.returncode, 'validator_summary': validate.stdout.strip()})
        if validate.returncode:
            write(ROOT / 'tooling/local-skill-failed-review.json', local_reviews)
            raise RuntimeError('Skill metadata validation failed: ' + name)
        smoke = ROOT / 'tooling/skill-smokes' / name
        request = {'family': selected[0]['family'], 'input': selected[0]['input']}
        write(smoke / 'positive-input.json', request)
        write(smoke / 'duplicate-member-input.json', '{"family":"first","family":"second","input":{}}\n')
        for kind, infile in [('positive', 'positive-input.json'), ('adverse', 'duplicate-member-input.json')]:
            call = subprocess.run([str(args.python), '-X', 'utf8', str(package / 'scripts' / runner), '--input', str(smoke / infile), '--output', str(smoke / (kind + '-output.json'))], capture_output=True, text=True, encoding='utf-8')
            if call.returncode:
                raise RuntimeError('Skill CLI failed: ' + name)
        positive = json.loads((smoke / 'positive-output.json').read_text(encoding='utf-8'))
        adverse = json.loads((smoke / 'adverse-output.json').read_text(encoding='utf-8'))
        assert canonical(positive) == canonical(selected[0]['expected_result'])
        assert adverse == {'error': 'duplicate_member'}
        receipt = {'schema': 'ghc.family.skill-smoke.v686.v4', 'skill': name, 'positive_pass': True, 'adverse_refused': True,
                   'negative_id': 'AR6864-SKILL-' + f'{len(receipts)+1:02}', 'same_owner_only': True, 'initial_adverse_credit': 0,
                   'runner': runner, 'source_proposal': selected[0]['proposal_id']}
        write(smoke / 'smoke-receipt.json', receipt)
        receipts.append(receipt)
    write(ROOT / 'tooling/local-skill-validation.json', {'schema': 'ghc.family.skill-validation.v686.v4', 'rows': local_reviews, 'count': len(local_reviews), 'all_pass': True})
    write(ROOT / 'tooling/skill-smoke-summary.json', receipts)

    # Recurrence guard added after the retained OP012 procedural lapse. This
    # source change is not a claim that it ran before the original promotions.
    meta_path = args.skill_root / 'ghc-family-meta-tool-box/scripts/ghc_family_meta_tool_box.py'
    spec = importlib.util.spec_from_file_location('promotion_meta', meta_path)
    meta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meta)
    catalogue = meta.build(ROOT.parents[2], ROOT)
    gate = [meta.promotion(catalogue, 'skill:' + skill['name']) for skill in plan['skills']]
    if not meta.validate(catalogue)['valid'] or any(row['state'] != 'ready' for row in gate):
        raise RuntimeError('Meta Tool Box promotion preflight refused')
    write(ROOT / 'tooling/prepromotion-meta-check.json', gate)

    # Each package is promoted only after every preceding local check succeeded.
    promoted = []
    for skill in plan['skills']:
        name = skill['name']
        package = ROOT / 'skills' / name
        target = args.skill_root / name
        if target.exists():
            raise RuntimeError('Global collision before promotion: ' + name)
        shutil.copytree(package, target)
        bindings = []
        for local in sorted(package.rglob('*')):
            if local.is_file():
                rel = local.relative_to(package)
                left, right = local.read_bytes(), (target / rel).read_bytes()
                assert left == right
                bindings.append({'relative_path': rel.as_posix(), 'sha256': hashlib.sha256(left).hexdigest(), 'bytes': len(left)})
        verify = subprocess.run([str(args.validator_python), '-X', 'utf8', str(args.creator_root / 'scripts/quick_validate.py'), str(target)], capture_output=True, text=True, encoding='utf-8')
        assert verify.returncode == 0
        promotion = {'skill': name, 'source_path': package.relative_to(ROOT.parents[2]).as_posix(), 'new_directory': True,
                     'byte_parity': True, 'global_validator_pass': True, 'file_count': len(bindings), 'bindings': bindings,
                     'hash_domain': 'raw source-checkout and global-installed bytes; Git manifests separately normalize text to LF',
                     'rollback': 'Select the prior validated source package without deleting or overwriting either package.'}
        write(ROOT / 'tooling/promotion-checks' / (name + '.json'), promotion)
        promoted.append(promotion)
    write(ROOT / 'tooling/global-promotion.json', {'schema': 'ghc.family.global-promotion.v686.v4', 'owner': 'Avelin Reed', 'phase': 'v686-v4', 'skills': promoted, 'skill_count': len(promoted), 'unique_runner_sources': 5, 'total_copied_files': sum(x['file_count'] for x in promoted), 'same_owner_only': True})
    print(json.dumps({'local_skills_validated': len(local_reviews), 'skill_smokes_passed': len(receipts), 'promoted_skills': len(promoted), 'copied_files': sum(x['file_count'] for x in promoted), 'unique_runner_sources': 5}))


if __name__ == '__main__':
    main()
