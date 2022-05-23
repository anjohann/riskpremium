def num_star_level(p_value):
  value = None
  if p_value < 0.01:
      value = "***"
  elif p_value < 0.05:
      value = "**"
  elif p_value < 0.1:
      value = "**"
  else:
      value = ""
  return value