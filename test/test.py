# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 128
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test PWM behavior")

    for duty_cycle, expected_high_cycles in ((0, 0), (128, 128), (255, 255)):
        dut.ui_in.value = duty_cycle
        high_cycles = 0

        for _ in range(256):
            await ClockCycles(dut.clk, 1)
            high_cycles += int(dut.uo_out.value) & 1

        assert high_cycles == expected_high_cycles
