from py.log import Producer

from xdist.slavemanage import parse_spec_config


class Scheduling:
    """
    This distributes the tests collected across all nodes so each test
    is run just once.  All nodes collect and submit the test suite and
    when all collections are received it is verified they are
    identical collections.  Then the collection gets divided up in
    chunks and chunks get submitted to nodes.  Whenever a node finishes
    an item, it calls ``.mark_test_complete()`` which will trigger the
    scheduler to assign more tests if the number of pending tests for
    the node falls below a low-watermark.

    When created, ``numnodes`` defines how many nodes are expected to
    submit a collection. This is used to know when all nodes have
    finished collection or how large the chunks need to be created.

    Attributes:

    :numnodes: The expected number of nodes taking part.  The actual
       number of nodes will vary during the scheduler's lifetime as
       nodes are added by the DSession as they are brought up and
       removed either because of a dead node or normal shutdown.  This
       number is primarily used to know when the initial collection is
       completed.

    :collection_is_completed: Boolean indication initial test
       collection is complete.  This is a boolean indicating all
       initial participating nodes have finished collection.  The
       required number of initial nodes is defined by ``.numnodes``.

    :nodes: A list of all nodes in the scheduler.

    :tests_finished: Return True if all tests have been executed by the nodes.

    :has_pending: Return True if there are pending test items.  This
       indicates that collection has finished and nodes are still
       processing test items, so this can be thought of as "the
       scheduler is active".
    """

    LOGGER_NAME = None

    def __init__(self, config, log=None):
        self.config = config
        self.numnodes = len(parse_spec_config(config))

        if log is None:
            self.log = Producer(self.LOGGER_NAME)
        else:
            self.log = getattr(log, self.LOGGER_NAME)

    def add_node(self, node):
        """Add a new node to the scheduler.

        Called by the ``DSession.slave_slaveready`` hook when it successfully
        bootstraps a new node.
        """
        raise NotImplementedError

    def remove_node(self, node):
        """Remove a node from the scheduler.

        This should be called either when the node crashed or at shutdown time.
        In the former case any pending items assigned to the node will be
        re-scheduled.

        Called by the hooks:

        - ``DSession.slave_slavefinished``.
        - ``DSession.slave_errordown``.

        Return the item being executed while the node crashed or None if the
        node has no more pending items.
        """
        raise NotImplementedError

    def add_node_collection(self, node, collection):
        """Add the collected test items from a node.

        Called by the hook:

        - ``DSession.slave_collectionfinish``.
        """
        raise NotImplementedError

    def mark_test_complete(self, node, item_index, duration=0):
        """Mark test item as completed by node.

        Called by the hook:

        - ``DSession.slave_testreport``.
        """
        raise NotImplementedError

    def schedule(self):
        """Initiate distribution of the test collection.

        If ``.collection_is_completed`` is True, this is called by the hook:

        - ``DSession.slave_collectionfinish``.
        """
        raise NotImplementedError
