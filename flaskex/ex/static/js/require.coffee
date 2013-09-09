vendors = {}

require = (location) ->
  if not location?
    return vendors

  lib = vendors[location]
  if lib
    return lib

require.addVendors = (vendorSets) ->
  for k, v of vendorSets
    vendors[k] = window[v]

window.require = require