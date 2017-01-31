SUBDIRS   := $(wildcard functions/*/)
ZIPS      := $(addsuffix .zip,$(subst functions,,$(subst /,,$(SUBDIRS))))
MAIN      = main.py
BUILD_DIR = build

echo:
	@echo $(value SUBDIRS)
	@echo $(value ZIPS)

#$(ZIPS): functions/%.zip : | %
#	zip BUILD_DIR/$@ functions/$*/${MAIN}

dist: $(ZIPS)

${BUILD_DIR}:
	mkdir ${BUILD_DIR}

manual: | ${BUILD_DIR}
	zip -j ${BUILD_DIR}/ami-s3-cleaner.zip functions/ami-s3-cleaner/${MAIN}
	zip -j ${BUILD_DIR}/check-ami-ready.zip functions/check-ami-ready/${MAIN}
	zip -j ${BUILD_DIR}/check-instance-ready.zip functions/check-instance-ready/${MAIN}
	zip -j ${BUILD_DIR}/check-inspector-assessment-run-complete.zip functions/check-inspector-assessment-run-complete/${MAIN}
	zip -j ${BUILD_DIR}/launch-instance.zip functions/launch-instance/${MAIN}
	zip -j ${BUILD_DIR}/parse-inspector-assessment-run-findings.zip functions/parse-inspector-assessment-run-findings/${MAIN}
	zip -j ${BUILD_DIR}/realtime-endpoint-shutdown.zip functions/realtime-endpoint-shutdown/${MAIN}
	zip -j ${BUILD_DIR}/start-inspector-assessment-run.zip functions/start-inspector-assessment-run/${MAIN}
	zip -j ${BUILD_DIR}/start-step-function.zip functions/start-step-function/${MAIN}
	zip -j ${BUILD_DIR}/tag-ec2-resource.zip functions/tag-ec2-resource/${MAIN}
	zip -j ${BUILD_DIR}/terminate-instance.zip functions/terminate-instance/${MAIN}

clean:
	rm $(ZIPS)