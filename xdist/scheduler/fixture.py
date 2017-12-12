from xdist.scheduler.load import LoadScheduling


class FixtureScheduling(LoadScheduling):
    LOGGER_NAME = 'fixturesched'

    def _send_tests(self, node, num):
        pending_indexed_tests = self._get_pending_tests()
        if not pending_indexed_tests:
            return

        pending_groups = self._get_groups(pending_indexed_tests)
        group = self._get_node_group(node)

        if group is None or group not in pending_groups:
            group = self._calculate_new_group_for_node(pending_groups)
            self.log("{}: new fixture group: '{}'".format(node, group))
            node.scheduler_group = group

        indices = self._filter_indices_by_group(pending_indexed_tests, group)[:num]
        if not indices:
            return

        self._remove_from_pending_tests(indices)
        self.node2pending[node].extend(indices)
        node.send_runtest_some(indices)

    def _calculate_new_group_for_node(self, pending_groups):
        ran_groups = self._get_ran_groups()
        unused_groups = pending_groups - ran_groups

        if unused_groups:
            return sorted(unused_groups)[0]

        return sorted(pending_groups)[0]

    def _get_pending_tests(self):
        return [
            (index, self.collection[index])
            for index in self.pending
        ]

    def _remove_from_pending_tests(self, indices):
        for index in reversed(indices):
            self.pending.remove(index)

    def _get_ran_groups(self):
        return set(
            group
            for group in [self._get_node_group(node) for node in self.nodes]
            if group is not None
        )

    def _get_groups(self, pending_indexed_tests):
        return set(
            self._get_test_group(tests)
            for _, tests in pending_indexed_tests
        )

    def _filter_indices_by_group(self, pending_indexed_tests, group):
        return [
             index
             for index, test in pending_indexed_tests
             if self._get_test_group(test) == group
        ]

    def _get_test_group(self, test):
        return test.split('::', 1)[0]

    def _get_node_group(self, node):
        return getattr(node, 'scheduler_group', None)
