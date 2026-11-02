# Coordinate Systems

## Convention
All coordinate systems are right-handed. Angles are in degrees, clockwise seen from above.

## Sevan Global
Basin-fixed, with:

- origin at the floater centre at the calm waterline
- x towards the wavemaker (irrespective of the floater's heading)
- y to port when facing the wavemaker
- z up

The floater heading is the direction of the floater's LQ, or of its local x-axis if no LQ is defined, measured
clockwise seen from above from Global x (towards the wavemaker); heading 0 means the LQ faces the waves. The floater
configuration gives the heading; its `turn` is the hull's turn from the campaign's LQ.

The derived sensors `XPOS_WL_GLOBAL`, `YPOS_WL_GLOBAL`, `ZPOS_WL_GLOBAL`, `ROLL_GLOBAL`, `PITCH_GLOBAL` and
`YAW_GLOBAL` are the motions in this system.

## The lab's systems
Each campaign states the lab's own axes as signed Sevan axes (`lab_axis_x/y/z`, e.g. `+x`, `-y`, `-z` for a lab with
y to starboard and z down), whether they turn with the set-up (`lab_global_turns`), and a body-fixed local system
where it differs (`lab_local_axis_x/y/z`, `lab_local_offset`, `lab_local_origin_x/y/z`, `lab_local_turns`), with
the LQ (`lq`), north (`north`, `north_type`) and the z origin (`z_origin`: the keel, a baseline, or the waterline or
COG of a floater configuration).

## Sensor positions
A sensor's `x`, `y`, `z` are in the lab's axes: the local ones for `position_reference` 'local', otherwise the
global ones. `z` is measured from the campaign's z origin, the calm waterline or the configuration's COG
(`position_z_reference`). A heading-locked position turns with the set-up. For a vector channel, `measures_frame`,
`measures_axis` and `measures_sign` say what it measures, and `dof` which motion.

`FloaterConfig.coordinates()` gives every sensor's position and measured direction in Sevan Global for that
configuration, as the API's coordinate viewer draws them.
