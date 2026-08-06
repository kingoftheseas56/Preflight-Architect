# Local Media Launch Slice 1 — Reference Code Part

**Status:** implementable reference code; uncompiled, untested, unexecuted, unadopted, and unverified.

**Colosseum basis:** `master@bb8eecb40eb8a50b7ded62f79035c555972c3fef`

This is one canonical segment of the interim Slice 1 bundle. The execution agent must inspect, adapt, compile, test, and runtime-validate before adoption.

## `native/CMakeLists.txt` candidate changes

```diff
diff --git a/native/CMakeLists.txt b/native/CMakeLists.txt
--- a/native/CMakeLists.txt
+++ b/native/CMakeLists.txt
@@ -1,3 +1,12 @@
     SearchHistoryStore.h
     SessionStore.h
+    localmedia/LocalMediaTypes.h
+    localmedia/LocalMediaTypes.cpp
+    localmedia/LocalMediaClassifier.h
+    localmedia/LocalMediaClassifier.cpp
+    localmedia/LocalMediaInspector.h
+    localmedia/LocalMediaInspector.cpp
+    localmedia/LocalMediaHandler.h
+    localmedia/LocalMediaRouter.h
+    localmedia/LocalMediaRouter.cpp
     AudioPairingStore.h
@@ -1,4 +1,15 @@
 target_include_directories(search_history_store_harness PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
 target_link_libraries(search_history_store_harness PRIVATE Qt6::Core)
 
+add_executable(local_media_contract_harness
+    ../tests/local_media_contract_harness.cpp
+    localmedia/LocalMediaTypes.cpp
+    localmedia/LocalMediaClassifier.cpp
+    localmedia/LocalMediaInspector.cpp
+    localmedia/LocalMediaRouter.cpp
+)
+target_include_directories(local_media_contract_harness
+    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
+target_link_libraries(local_media_contract_harness PRIVATE Qt6::Core)
+
 add_executable(background_work_coordinator_harness
```

## `tests/CMakeLists.txt` candidate changes

```diff
diff --git a/tests/CMakeLists.txt b/tests/CMakeLists.txt
--- a/tests/CMakeLists.txt
+++ b/tests/CMakeLists.txt
@@ -1,4 +1,5 @@
 colosseum_register_harness(comicreader_cache_harness     unit)
 colosseum_register_harness(biblio_catalog_logic_harness  unit)
+colosseum_register_harness(local_media_contract_harness   unit;local-media)
 
 # ── Qt Test targets (slice 3+) ────────────────────────────────────────────────
```
