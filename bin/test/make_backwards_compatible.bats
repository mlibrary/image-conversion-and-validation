@test "has help text" {
  run ./bin/make_backwards_compatible -h
  [ "$status" -eq 0 ]
}
