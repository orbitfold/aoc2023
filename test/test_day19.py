from aoc2023.day19_b import Rule, Part, Workflow

def test_rule():
    part = Part()
    rule = Rule("s<1351:px")
    result = rule.check_part(part)
    assert(result == ('px', Part((1, 4000), (1, 4000), (1, 4000), (1, 1350)), Part((1, 4000), (1, 4000), (1, 4000), (1351, 4000))))
    rule = Rule("m>838:A")
    result = rule.check_part(part)
    assert(result == ('A', Part((1, 4000), (839, 4000), (1, 4000), (1, 4000)), Part((1, 4000), (1, 838), (1, 4000), (1, 4000))))
    rule = Rule("pv")
    result = rule.check_part(part)
    assert(result == ('pv', part, None))
    rule = Rule('A')
    result = rule.check_part(part)
    assert(result == ('A', part, None))
    rule = Rule('R')
    result = rule.check_part(part)
    assert(result == ('R', part, None))

def test_workflow():
    part = Part()
    workflow = Workflow("px{a<2006:qkq,m>2090:A,rfg}")
    result = workflow.check_part(part)
    assert(result == {'qkq': Part(x=(1, 4000), m=(1, 4000), a=(1, 2005), s=(1, 4000)), 'A': Part(x=(1, 4000), m=(2091, 4000), a=(2006, 4000), s=(1, 4000)), 'rfg': Part(x=(1, 4000), m=(1, 2090), a=(2006, 4000), s=(1, 4000))})

