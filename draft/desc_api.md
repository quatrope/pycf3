Test implemented


## `calculate_distance` tests

- `test_equatorial_calculate_distance_vel_EQ_10`:
  Validates the correct response of call *calculate_distance* with equatorial
  coordinates (`ra` and `dec`) and `velocity=10`.

- `test_galactic_calculate_distance_vel_EQ_10`:
  Validates the correct response of call *calculate_distance* with galactic
  coordinates (`glon` and `glat`) and `velocity=10`.

- `test_sgalactic_calculate_distance_vel_EQ_10`:
  Validates the correct response of call *calculate_distance* with supergalactic
  coordinates (`gsgl` and `sgb`) and `velocity=10`.


## `calculate_velocity` tests

- `test_equatorial_calculate_velocity_dis_EQ_10`:
  Validates the correct response of call *calculate_velocity* with equatorial
  coordinates (`ra` and `dec`) and `distance=10`.

- `test_galactic_calculate_velocity_dis_EQ_10`:
  Validates the correct response of call *calculate_velocity* with galactic
  coordinates (`glon` and `glat`) and `distance=10`.

- `test_sgalactic_calculate_velocity_dis_EQ_10`:
  Validates the correct response of call *calculate_velocity* with supergalactic
  coordinates (`gsgl` and `sgb`) and `distance=10`.


## Velocity or distance == 0 tests

- `test_calculate_distance_velocity_eq_0`: call the method
  *calculate_distance* with the `velocity=0` raises a `ValueError`.

- `test_calculate_velocity_distance_eq_0`: call the method
  *calculate_velocity* with the `distance=0` raises a `ValueError`.


## Velocity or distance < 0 tests

- `test_calculate_velocity_distance_lt_0`: call the method
  *calculate_velocity* with the `distance < 0` raises a `ValueError`.

- `test_calculate_distance_velocity_lt_0`: call the method
  *calculate_distance* with the `velocity < 0` raises a `ValueError`.


## alpha or delta not a number tests

- `test_calculate_velocity_alpha_not_number`: call the method
  *calculate_velocity* with `ra`, `glon` or `sgl` equals to something different
  than a integer or float raises a `TypeError`.

- `test_calculate_velocity_delta_not_number`: call the method
  *calculate_velocity* with `dec`, `glat` or `sgb` equals to something different
  than a integer or float raises a `TypeError`.

- `test_calculate_distance_alpha_not_number`: call the method
  *calculate_distance* with `ra`, `glon` or `sgl` equals to something different
  than a integer or float raises a `TypeError`.

- `test_calculate_distance_delta_not_number`: call the method
  *calculate_distance* with `dec`, `glat` or `sgb` equals to something different
  than a integer or float raises a `TypeError`.


## velocity or distance not a number tests

- `test_calculate_velocity_distance_not_number`: call the method
  *calculate_velocity* with `distance` equals to something different
  than a integer or float raises a `TypeError`.

- `test_calculate_distance_velocity_not_number`: call the method
  *calculate_distance* with `velocity` equals to something different
  than a integer or float raises a `TypeError`.


## Alpha > 90 or alpha < -90 tests

- `test_calculate_velocity_alpha_gt_90`: call the method
  *calculate_velocity* with `ra, glon sgl > 90` raises a `ValueError`.

- `test_calculate_velocity_alpha_lt_m90`: call the method
  *calculate_velocity* with `ra, glon sgl < -90` raises a `ValueError`.

- `test_calculate_distance_alpha_gt_90`: call the method
  *calculate_distance* with `ra, glon sgl > 90` raises a `ValueError`.

- `test_calculate_distance_alpha_lt_m90`: call the method
  *calculate_distance* with `ra, glon sgl < -90` raises a `ValueError`.

## Mix coordinates tests

- `test_calculate_velocity_mix_coordinate_system`: Call the method
  *calculate_velocity* with mixed coordinate sistem (using `ra` and `glon`
  for example) Raises a `pycf3.MixedCoordinateSystemError`.

- `test_calculate_distance_mix_coordinate_system`: Call the method
  *calculate_distance* with mixed coordinate sistem (using `ra` and `glon`
  for example) Raises a `pycf3.MixedCoordinateSystemError`.

- `test_calculate_velocity_multiple_alpha`: call the method *calculate_velocity*
  with multiple alpha (`ra`, `glat` for example) raises a `pycf3.MixedCoordinateSystemError`.

- `test_calculate_velocity_multiple_delta`:
  call the method *calculate_velocity*
  with multiple delta (`dec`, `glat` for example) raises a `pycf3.MixedCoordinateSystemError`.

- `test_calculate_distance_multiple_alpha`:
  call the method *calculate_distance*
  with multiple alpha (`ra`, `glat` for example) raises a `pycf3.MixedCoordinateSystemError`.

- `test_calculate_distance_multiple_delta`: call the method *calculate_distance*
  with multiple delta (`dec`, `glat` for example) raises a `pycf3.MixedCoordinateSystemError`.