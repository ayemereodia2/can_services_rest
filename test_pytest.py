import inc_dec

def test_increment():
    assert inc_dec.increment(3) == 4

# test designed to fail for demo purposes
def test_decrement():
    assert inc_dec.decrement(3) == 2