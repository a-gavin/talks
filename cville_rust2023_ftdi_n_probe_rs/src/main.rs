use anyhow::Result;
use probe_rs::{
    Probe
};

// Adapted from the probe-rs raw_dap_access.rs example
fn main() -> Result<()> {
    // Get a list of all available debug probes.
    let probes = Probe::list_all();

    // Use the first probe found.
    let mut probe = probes[0].open()?;
    probe.attach_to_unspecified()?;
    let mut iface = probe.try_into_riscv_interface().unwrap();

    // Read and print out idcode of target
    let idcode = iface.read_idcode()?;
    println!("Chip idcode: {:#x}", idcode);

    Ok(())
}