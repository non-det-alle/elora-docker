/*
 * Set of utilities to keep main example files more clean.
 */

#include "ns3/lora-helper.h"
#include "ns3/lora-interference-helper.h"

#include <csignal>
#include <vector>

using namespace ns3;
using namespace lorawan;

namespace ns3
{

/**
 * Clusters info (% devices, PDR required)
 */
using cluster_t = std::vector<std::pair<double, double>>;

/**
 * Parse clusters' info from string
 */
cluster_t ParseClusterInfo(std::string s);

/**
 * \brief Computes total deployment area
 *
 * Computes total deployment area in range of gateways placed with
 * complete radial hexagonal tiling. This assumes that the maximum
 * range devices are placed from a gateway is the side of hexagons.
 *
 * \param range Maximum device range from center of a gateway [m]
 * \param rings Number of rings of hexagons (central gateway = first ring)
 *
 * \return Deployment area [km^2]
 */
double ComputeArea(double range, int rings);

/**
 * Possible interference matrices
 */
const std::unordered_map<std::string, LoraInterferenceHelper::IsolationMatrix> sirMap = {
    {"CROCE", LoraInterferenceHelper::CROCE},
    {"GOURSAUD", LoraInterferenceHelper::GOURSAUD},
    {"ALOHA", LoraInterferenceHelper::ALOHA}};

/**
 * Print initial configuration
 */
void PrintConfigSetup(int nDevs, double range, int rings, std::vector<int>& devPerSF);

/**
 * Setup action on interrupt
 */
void OnInterrupt(sighandler_t action);

/**
 * Granularities of the tracing system
 */
const std::unordered_map<std::string, LoraHelper::TraceLevel> traceLevelMap = {
    {"PKT", LoraHelper::PKT},
    {"DEV", LoraHelper::DEV},
    {"SF", LoraHelper::SF},
    {"GW", LoraHelper::GW},
    {"NET", LoraHelper::NET}};

std::vector<LoraHelper::TraceLevel> ParseTraceLevels(std::string s);

const std::map<EndDeviceLoraPhy::State, std::string> stateMap = {
    {EndDeviceLoraPhy::State::SLEEP, "SLEEP"},
    {EndDeviceLoraPhy::State::TX, "TX"},
    {EndDeviceLoraPhy::State::STANDBY, "STANDBY"},
    {EndDeviceLoraPhy::State::RX, "RX"}};

void OnStateChange(EndDeviceLoraPhy::State oldS, EndDeviceLoraPhy::State newS);

} // namespace ns3
