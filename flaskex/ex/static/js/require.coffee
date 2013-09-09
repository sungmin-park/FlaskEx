class Requirefy
  constructor: ->
    @vendors = {}

  require: (location) =>
    switch location
      when 'streamline/lib/callbacks/runtime' then Streamline.runtime
      when 'streamline/lib/callbacks/builtins' then Streamline.builtins
      when 'streamline/lib/globals' then Streamline.globals
      when 'streamline/lib/util/future' then Streamline.future
      else
        lib = @vendors[location]
        if not lib
          throw Error "Cannot find #{location}"
        lib.exports

  addVendors: (vendorSets) ->
    for k, v of vendorSets
      @vendors[k] = exports: window[v]

  regist: (name, fn, ctx=window) ->
    module = exports: {}
    @vendors[name] = module
    fn.call(ctx, name, module, module.exports)

window.requirefy = new Requirefy
window.require = window.requirefy.require

# Streamlinejs support
# https://github.com/Sage/streamlinejs/blob/master/lib/callbacks/require-stub.js
# default filename
window.__filename = '' + window.location
window.Streamline = globals: {}
# streamlinejs uses process nextTic
window.process = nextTick: (func) ->
  setTimeout func, 0
# streamlinejs's default error handler
# 어플의 EntryPoint에서 사용된다.
# 기본적으로 callback으로 전달되기 때문에
# application이 시작되는 부분에서 throw 하기 위해서 필요하다.
window.autoThrow = (err) ->
  if err?
    console.error err.stack
    throw err