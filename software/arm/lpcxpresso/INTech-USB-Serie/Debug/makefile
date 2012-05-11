################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: INTech-USB-Serie.axf

dependents:
	-cd C:/Users/Nils/Documents/LPCXpresso_4.2.0_264/workspace/CMSISv2_LPC17xx/Debug && $(MAKE) clean all

# Tool invocations
INTech-USB-Serie.axf: $(OBJS) $(USER_OBJS) C:/Users/Nils/Documents/LPCXpresso_4.2.0_264/workspace/CMSISv2_LPC17xx/Debug/libCMSISv2_LPC17xx.a
	@echo 'Building target: $@'
	@echo 'Invoking: MCU Linker'
	arm-none-eabi-gcc -nostdlib -L"C:\Users\Nils\Documents\LPCXpresso_4.2.0_264\workspace\CMSISv2_LPC17xx\Debug" -Xlinker -Map=INTech-USB-Serie.map -Xlinker --gc-sections -mcpu=cortex-m3 -mthumb -T INTech-USB-Serie_Debug.ld -o"INTech-USB-Serie.axf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(OBJS)$(C_DEPS)$(EXECUTABLES) INTech-USB-Serie.axf
	-@echo ' '

post-build:
	-@echo 'Performing post-build steps'
	-arm-none-eabi-size INTech-USB-Serie.axf; arm-none-eabi-objcopy -O binary INTech-USB-Serie.axf INTech-USB-Serie.bin ; checksum -p LPC1769 -d INTech-USB-Serie.bin;
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build
C:/Users/Nils/Documents/LPCXpresso_4.2.0_264/workspace/CMSISv2_LPC17xx/Debug/libCMSISv2_LPC17xx.a:

-include ../makefile.targets
