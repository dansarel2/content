import os
from release_notes_generator import get_release_notes_dict, generate_release_notes_summary

TEST_DATA_PATH = 'Tests/scripts/infrastructure_tests/tests_data/RN_tests_data'

VERSION = 'VERSION'
ASSET_ID = 'ASSET_ID'


def check_assertions_on_release_notes_dict(rn_dict):
    assert '1.0.1' not in rn_dict['FakePack1'].keys()
    assert '1.1.0' in rn_dict['FakePack1'].keys()
    assert '2.0.0' in rn_dict['FakePack1'].keys()

    assert '1.0.1' not in rn_dict['FakePack2'].keys()
    assert '1.1.0' in rn_dict['FakePack2'].keys()


def check_assertions_on_release_notes_summary(rn_summary):
    assert '# Cortex XSOAR Content Release Notes for version {} ({})\n'.format(VERSION, ASSET_ID)

    assert '## FakePack1 Pack v1.0.1' not in rn_summary
    assert '- __FakePack1_Integration1__' in rn_summary
    assert '## FakePack1 Pack v1.1.0' in rn_summary
    assert 'This is a fake minor release note.' in rn_summary
    assert '## FakePack1 Pack v2.0.0' in rn_summary
    assert 'This is a fake major release note.' in rn_summary
    assert '- __FakePack2_Script1__' in rn_summary


def test_release_notes_generator():
    """
    Given
    - A repository of two packs updates and release notes:
      - FakePack1 with versions 1.0.1, 1.1.0 and 2.0.0
      - FakePack2 with versions 1.0.1 and 1.1.0

    When
    - Generating a release notes summary file.

    Then
    - Ensure release notes generator creates a valid summary, by checking:
      - the output of get_release_notes_dict() is a valid dict of (pack_name, dict(pack_version, release_note))
      - the format of the release notes summary is as expected.
      - the summary does not contain release notes that should be ignored.
    """
    release_notes_files = [
        os.path.join(TEST_DATA_PATH, 'FakePack1', 'ReleaseNotes', '1_0_1.md'),
        os.path.join(TEST_DATA_PATH, 'FakePack1', 'ReleaseNotes', '1_1_0.md'),
        os.path.join(TEST_DATA_PATH, 'FakePack1', 'ReleaseNotes', '2_0_0.md'),
        os.path.join(TEST_DATA_PATH, 'FakePack2', 'ReleaseNotes', '1_0_1.md'),
        os.path.join(TEST_DATA_PATH, 'FakePack2', 'ReleaseNotes', '1_1_0.md')
    ]

    rn_dict = get_release_notes_dict(release_notes_files)
    check_assertions_on_release_notes_dict(rn_dict)

    rn_summary = generate_release_notes_summary(rn_dict, VERSION, ASSET_ID)
    check_assertions_on_release_notes_summary(rn_summary)