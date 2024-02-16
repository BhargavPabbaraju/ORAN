def section2():
    rb_value = "65%"

    throughput_impact = "30%"
    throughput_baseline = "35%"
    power_impact = "50%"
    power_baseline = "59%"

    schedule_policy = "Round Robin"

    return {
        'rb_value': rb_value,
        'throughput_impact': throughput_impact,
        'throughput_baseline': throughput_baseline,
        'power_impact': power_impact,
        'power_baseline': power_baseline,
        'schedule_policy': schedule_policy
    }