"""Test the TcEx API Snippets."""
# first-party
from tcex.api.tc.v3.tql.tql_operator import TqlOperator
from tests.api.tc.v3.v3_helpers import TestV3, V3Helper


class TestUserSnippets(TestV3):
    """Test TcEx API Interface."""

    v3 = None

    def setup_method(self):
        """Configure setup before all tests."""
        print('')  # ensure any following print statements will be on new line
        self.v3_helper = V3Helper('users')
        self.v3 = self.v3_helper.v3
        self.tcex = self.v3_helper.tcex

    def test_user_get_all(self):
        """Test snippet"""
        # Begin Snippet
        for user in self.tcex.v3.users():
            print(user.model.dict(exclude_none=True))
        # End Snippet

    def test_user_tql_filter(self):
        """Test snippet"""
        # Begin Snippet
        users = self.tcex.v3.users()
        users.filter.first_name(TqlOperator.EQ, 'Robin')
        # users.filter.group_id(TqlOperator.EQ, 'Robin')
        users.filter.last_name(TqlOperator.EQ, 'Sparkles')
        users.filter.user_name(TqlOperator.EQ, 'rsparkles')
        for user in users:
            print(user.model.dict(exclude_none=True))
        # End Snippet

    def test_user_get_by_id(self):
        """Test snippet"""
        # Begin Snippet
        user = self.tcex.v3.user(id=5)
        user.get()
        print(user.model.dict(exclude_none=True))
        # End Snippet
