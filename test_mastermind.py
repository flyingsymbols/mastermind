import mastermind as M

def test_color_to_num():
    assert M.num_to_colors(M.colors_to_num('OOGP')) == 'OOGP'
