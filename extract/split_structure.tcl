# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# The script to split the structure from dcd trajectory
# file
# ---------------------------------------------------------

mol new ala_sol.psf
mol addfile ala_prod4.dcd
set num_frames [molinfo top get numframes]
for {set i 0} {$i < $num_frames} {incr i} {
set frame $i
set sel [atomselect top protein frame $i]
$sel writexyz $i.xyz
$sel delete
}