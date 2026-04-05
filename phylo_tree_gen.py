from Bio import Phylo

cd28_g_tree = Phylo.read("sequenceList_cd28_g.dnd", "newick")
ctla4_g_tree = Phylo.read("sequenceList_ctla4_g.dnd", "newick")
icos_g_tree = Phylo.read("sequenceList_icos_g.dnd", "newick")
pd1_g_tree = Phylo.read("sequenceList_pd1_g.dnd", "newick")
cd28_p_tree = Phylo.read("sequenceList_cd28_p.dnd", "newick")
ctla4_p_tree = Phylo.read("sequenceList_ctla4_p.dnd", "newick")
icos_p_tree = Phylo.read("sequenceList_icos_p.dnd", "newick")
pd1_p_tree = Phylo.read("sequenceList_pd1_p.dnd", "newick")

# draw ASCII plots
print("#### CD28 GENE ####")
Phylo.draw_ascii(cd28_g_tree)

print("\n\n#### CTLA4 GENE ####")
Phylo.draw_ascii(ctla4_g_tree)

print("\n\n#### ICOS GENE ####")
Phylo.draw_ascii(icos_g_tree)

print("\n\n#### PD1 GENE ####")
Phylo.draw_ascii(pd1_g_tree)

print("#### CD28 PROTEIN ####")
Phylo.draw_ascii(cd28_p_tree)

print("\n\n#### CTLA4 PROTEIN ####")
Phylo.draw_ascii(ctla4_p_tree)

print("\n\n#### ICOS PROTEIN ####")
Phylo.draw_ascii(icos_p_tree)

print("\n\n#### PD1 PROTEIN ####")
Phylo.draw_ascii(pd1_p_tree)

# draw nice plots (displayed one-by-one)
Phylo.draw(cd28_g_tree)
Phylo.draw(ctla4_g_tree)
Phylo.draw(icos_g_tree)
Phylo.draw(pd1_g_tree)
Phylo.draw(cd28_p_tree)
Phylo.draw(ctla4_p_tree)
Phylo.draw(icos_p_tree)
Phylo.draw(pd1_p_tree)